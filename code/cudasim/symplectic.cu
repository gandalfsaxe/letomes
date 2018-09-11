#include <omp.h>
#include <cuda_runtime.h>
#include <helper_cuda.h>
#include <stdio.h>
#include <math.h>

#include "symplectic.h"
#include "constants.h"

__device__
inline double pdot_denominator1(double x, double y)
{
    return ((x + K) * (x + K) + y * y) * sqrt((x + K) * (x + K) + y * y);
}

__device__
inline double pdot_denominator2(double x, double y)
{
    return ((x - 1 + K) * (x - 1 + K) + y * y) * 
        sqrt((x - 1 + K) * (x - 1 + K) + y * y);
}

// from position and momentum vectors, returns generalized momentum, nondimensionalized
__device__
inline double get_pdot_x(double x, double y, double p_y)
{
    return p_y - ((1 - K) * (x + K)) / pdot_denominator1(x, y) + 
        K * (x - 1 + K) / pdot_denominator2(x, y);
}

__device__
inline double get_pdot_y(double x, double y, double p_x)
{
    return -p_x - (1 - K) * y / pdot_denominator1(x, y) - 
        K * y / pdot_denominator2(x, y);
}

__device__
inline double get_v_x(double y, double p_x)
{
    return p_x + y;
}

__device__
inline double get_v_y(double x, double p_y)
{
    return p_y - x;
}

// Runs symplectic adaptive euler-verlet algorithm
// All values are with nondimensionalized units
__device__
void symplectic(double x0,
                double y0,
                double p0_x,
                double p0_y,
                double maxDuration,
                double maxIter,
                double* score,
                bool* success
                )
{
    //success[0] = 0
    double h = h_DEFAULT;
    double h_min = h_MIN;
    double t = 0;  // total elapsed time
    double x = x0;
    double y = y0;
    double p_x = p0_x;
    double p_y = p0_y;
    //path_storage = []
    //path_storage.append([x, y, p_x, p_y, h])
    double smallest_distance = 1e6;
    double Dv = 0;
    int iteration_count = 0;

    double target_orbital_radius = LLO_RADIUS;
    double target_orbital_velocity = LLO_VELOCITY;
    double target_position_x = LUNAR_POSITION_X;
    double target_position_y = 0;
    double target_orbital_velocity_nondim = target_orbital_velocity / UNIT_VELOCITY;

    double earth_orbital_radius = LEO_RADIUS;
    double earth_orbital_velocity = LEO_VELOCITY;
    double earth_position_x = EARTH_POSITION_X;
    double earth_position_y = 0;
    double earth_celestial_radius = EARTH_RADIUS;
    double orbital_radius_lower_bound =
        (target_orbital_radius - ORBITAL_TOLERANCE) / UNIT_LENGTH;
    double orbital_radius_upper_bound = 
        (target_orbital_radius + ORBITAL_TOLERANCE) / UNIT_LENGTH;
    float too_far_away = 4 / UNIT_LENGTH;

    while (t < maxDuration)
    {
        if (iteration_count > maxIter)
        {
            // printf("exceeded max iterations, stranded in space!\n");
            printf(".");
            success[0] = false;
            score[0] = smallest_distance;
            return; //return path_storage
        }

        //========= EULER STEP ==========
        // Take a single time step of the symplectic Euler algorithm
        double x_euler, y_euler; //, p_x_euler, p_y_euler;
        {
            //printf("input = %f %f %f %f %f\n", h, x, y, p_x, p_y);
            // Step 1
            double v_x = get_v_x(y, p_x);
            double x_ = (x + (v_x + p_y * h) * h) / (1.0 + h * h);
            // Step 2
            double v_y = get_v_y(x_, p_y);
            double y_ = y + v_y * h;
            // Step 3
            //double pdot_x = get_pdot_x(x_, y_, p_y);
            //double pdot_y = get_pdot_y(x_, y_, p_x);
            //double p_x_ = p_x + pdot_x * h;
            //double p_y_ = p_y + pdot_y * h;
            x_euler = x_;
            y_euler = y_;
            //p_x_euler = p_x_;
            //p_y_euler = p_y_;
            //printf("%.15f %.15f %.15f %.15f\n", x_, v_x, pdot_x, p_x_);
            //printf("%.15f %.15f %.15f %.15f\n", y_, v_y, pdot_y, p_y_);
        }
        //printf("euler: %.15f %.15f %.15f %.15f\n", x_euler, y_euler, p_x_euler, p_y_euler);

        //========= VERLET STEP ==========
        // Takes a half step, then another half step in the symplectic Verlet algorithm"""
        double x_verlet, y_verlet, p_x_verlet, p_y_verlet;
        {
            double hh = 0.5 * h;
            double denominator = 1.0 / (1.0 + hh * hh);
            // Step 1
            double v_x = get_v_x(y, p_x);
            double x_ = (x + (v_x + p_y * hh) * hh) * denominator;
            // Step 2
            double v_y = get_v_y(x_, p_y);
            double y_ = y + v_y * hh;
            // Step 2
            double pdot_x = get_pdot_x(x_, y_, p_y);
            double pdot_y = get_pdot_y(x_, y_, p_x);
            double p_x_ = (p_x + (2.0 * pdot_x + (2 * pdot_y + p_x) * hh) * hh) * denominator;
            double p_y_ = p_y + (pdot_y + get_pdot_y(x_, y_, p_x_)) * hh;
            // TODO: mixed, what's correct? Derive theory
            // Step 3
            v_x = get_v_x(y_, p_x_);
            v_y = get_v_y(x_, p_y_);
            x_ += v_x * hh;
            y_ += v_y * hh;
            x_verlet = x_;
            y_verlet = y_;
            p_x_verlet = p_x_;
            p_y_verlet = p_y_;
        }
        //printf("verlet: %.15f %.15f %.15f %.15f\n", x_verlet, y_verlet, p_x_verlet, p_y_verlet);

        double err = sqrt((
            (x_verlet - x_euler) * (x_verlet - x_euler) + 
            (y_verlet - y_euler) * (y_verlet - y_euler)) / 
            (x_verlet * x_verlet + y_verlet * y_verlet));
        //printf("err = %.15g\n", err);

        if (err < STEP_ERROR_TOLERANCE || h <= h_min)
        {
            iteration_count += 1;
            x = x_verlet;
            y = y_verlet;
            p_x = p_x_verlet;
            p_y = p_y_verlet;
            t += h;
            h = max(h_min, h * max(0.1, 0.8 * sqrt(STEP_ERROR_TOLERANCE / err)));
            //printf("accept step h=%.15lf, err=%.15lf, x = %.15lf, t = %.15lf\n", h, err, x, t);
            // Accept the step only if the weighted error is no more than the
            // tolerance tol.  Estimate an h that will yield an error of tol on
            // the next step and use 0.8 of this value to avoid failures.
        }
        else
        {
            h = max(h_min, h / 2);
            //printf("deny step h=%.15lf, err=%.15lf, x = %.15lf, t = %.15lf\n", h, err, x, t);
        }

        // Are we nearly there yet? (calculate distance)
        double target_distance_x = x - target_position_x;
        double target_distance_y = y - target_position_y;
        double target_distance = sqrt(target_distance_x * target_distance_x + target_distance_y * target_distance_y);
        if (target_distance > too_far_away)
        {
            // printf("we are way too far away, stranded in space!\n");
            printf("|");
            success[0] = false;
            score[0] = smallest_distance;
            return; //path_storage
        }
        smallest_distance = min(smallest_distance, target_distance);

        // For real though, are we there yet? (did we actually hit?)
        if (smallest_distance >= orbital_radius_lower_bound &&
            smallest_distance <= orbital_radius_upper_bound)
        {
            // SUCCESS! We are in orbit range
            // current velocity vector
            double v_x = p_x + y;
            double v_y = p_y - x;

            // We adjust our velocity so the spacecraft enters a closed circular orbit.
            // We treat target_distance as a vector from spacecraft to target

            // project velocity vector onto radial direction unit-vector. This is what we
            // want to subtract from the velocity vector to obtain the tangental component (closed circular orbit)
            double v_radial = (v_x * target_distance_x + v_y * target_distance_y) 
                / target_distance;

            // phi is the angle of the radial vector
            double cos_phi = target_distance_x / target_distance;
            double sin_phi = target_distance_y / target_distance;
            // project radial velocity component to x and y axes.
            v_x = v_x - v_radial * cos_phi;
            v_y = v_y - v_radial * sin_phi;
            double v_magnitude = sqrt(v_x * v_x + v_y * v_y);

            // Delta-V for the maneuver
            Dv = sqrt(v_radial * v_radial + 
                      (v_magnitude - target_orbital_velocity_nondim) * (v_magnitude - target_orbital_velocity_nondim));
            //printf("SUCCESS! duration=%8.6g, Dv=%17.15g, iteration_count=%-10i\n", t * UNIT_TIME, Dv, iteration_count);
            printf("O");
            success[0] = true;
            score[0] = Dv;
            return; // path_storage
        }

        //path_storage.append([x, y, p_x, p_y, h])
        //printf("[x, y, p_x, p_y, h] = [%.15g, %.15g, %.15g, %.15g, %.15g]\n", x, y, p_x, p_y, h);

        // check if we somehow accidentally struck the earth (whoops)
        double earth_distance_sqr =
            (x - earth_position_x) * (x - earth_position_x) + 
            (y - earth_position_y) * (y - earth_position_y);
        // not necessarily a crash, but we don't want paths that take us to such risky territories
        double critical_distance = (earth_celestial_radius / UNIT_LENGTH) * (earth_celestial_radius / UNIT_LENGTH);
        if (earth_distance_sqr < critical_distance)
        {
            // printf("Anga crashed into the earth!\n");
            printf("X");
            success[0] = false;
            score[0] = smallest_distance;
            return; // path_storage
        }

    }
    //printf("exceeded max duration!\n");
    //printf("smallest distance=%g, orbital_radius_lower_bound=%g, orbital_radius_upper_bound=%g\n", smallest_distance, orbital_radius_lower_bound, orbital_radius_upper_bound);
    success[0] = false;
    score[0] = smallest_distance;
    return; // path_storage
}
