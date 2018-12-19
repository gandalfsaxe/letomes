#include "constants.h"
#include "coordinate_system.h"
#include "equations_of_motion.h"
#include "equations_of_physics.h"

#include <omp.h>
#include <cuda_runtime.h>
#include <stdio.h>
#include <math.h>

extern "C" {

    void initial_conditions(int nDays,
                            double* days,
                            int nBurndvs,
                            double* burndvs,
                            int nTilts,
                            double* tilts,
                            double altitude,
                            int size_ephemerides,
                            double* earth_R, double* earth_theta, double* earth_phi,
                            double* mars_R, double* mars_theta, double* mars_phi,
                            double* days_out,
                            double* Qs_out,
                            double* Bs_out)
    {
        #pragma omp parallel for
        for (int n = 0; n < nDays * nBurndvs * nTilts; ++n)
        {
            int i = n / (nBurndvs * nTilts);
            int m = n % (nBurndvs * nTilts);
            int j = m / nTilts;
            int k = m % (nTilts);
            int idx = days[i];
            double d = days[i] - idx;
            idx += 1;
            //double R_sun = SUN_R;
            //double theta_sun = SUN_THETA * M_PI / 180.0;
            //double phi_sun = SUN_PHI;
            double R_earth = lerp(earth_R[idx], earth_R[idx + 1], d);
            double theta_earth = lerp(earth_theta[idx], earth_theta[idx + 1], d);
            double phi_earth = lerp(earth_phi[idx], earth_phi[idx + 1], d);

            double x_earth, y_earth, z_earth;
            spherical2cartesian(R_earth, theta_earth, phi_earth, &x_earth, &y_earth, &z_earth);

            double x0_earth, y0_earth, z0_earth, x1_earth, y1_earth, z1_earth;
            spherical2cartesian(earth_R[idx], earth_theta[idx], earth_phi[idx], &x0_earth, &y0_earth, &z0_earth);
            spherical2cartesian(earth_R[idx + 1], earth_theta[idx + 1], earth_phi[idx + 1], &x1_earth, &y1_earth, &z1_earth);

            double vx_earth = (x1_earth - x0_earth) * UNIT_TIME / DAY;
            double vy_earth = (y1_earth - y0_earth) * UNIT_TIME / DAY;
            double vz_earth = (z1_earth - z0_earth) * UNIT_TIME / DAY;
            double norm_v_earth = sqrt(vx_earth * vx_earth +
                                       vy_earth * vy_earth +
                                       vz_earth * vz_earth);
            double vx_earth_unit = vx_earth / norm_v_earth;
            double vy_earth_unit = vy_earth / norm_v_earth;
            double vz_earth_unit = vz_earth / norm_v_earth;

            double x_orbital_plane_unit = y_earth * vz_earth - z_earth * vy_earth;
            double y_orbital_plane_unit = z_earth * vx_earth - x_earth * vz_earth;
            double z_orbital_plane_unit = x_earth * vy_earth - y_earth * vx_earth;
            double norm_orbital_plane_unit = sqrt(x_orbital_plane_unit * x_orbital_plane_unit +
                                             y_orbital_plane_unit * y_orbital_plane_unit +
                                             z_orbital_plane_unit * z_orbital_plane_unit);
            x_orbital_plane_unit /= norm_orbital_plane_unit;
            y_orbital_plane_unit /= norm_orbital_plane_unit;
            z_orbital_plane_unit /= norm_orbital_plane_unit;

            double x_leo_unit = -(y_orbital_plane_unit * vz_earth - z_orbital_plane_unit * vy_earth);
            double y_leo_unit = -(z_orbital_plane_unit * vx_earth - x_orbital_plane_unit * vz_earth);
            double z_leo_unit = -(x_orbital_plane_unit * vy_earth - y_orbital_plane_unit * vx_earth);
            double norm_leo_unit = sqrt(x_leo_unit * x_leo_unit +
                                        y_leo_unit * y_leo_unit +
                                        z_leo_unit * z_leo_unit);
            x_leo_unit /= norm_leo_unit;
            y_leo_unit /= norm_leo_unit;
            z_leo_unit /= norm_leo_unit;

            double x = x_leo_unit * (EARTH_RADIUS + altitude) / UNIT_LENGTH + x_earth;
            double y = y_leo_unit * (EARTH_RADIUS + altitude) / UNIT_LENGTH + y_earth;
            double z = z_leo_unit * (EARTH_RADIUS + altitude) / UNIT_LENGTH + z_earth;

            double e_speed = UNIT_VELOCITY * norm_v_earth;
            double leo_speed = get_circular_orbit_speed(altitude);
            double burn_speed = burndvs[j];

            double vx_leo_unit, vy_leo_unit, vz_leo_unit;
            rotate(vx_earth_unit, vy_earth_unit, vz_earth_unit,
                   x_leo_unit, y_leo_unit, z_leo_unit,
                   &vx_leo_unit, &vy_leo_unit, &vz_leo_unit,
                   tilts[k]);
            double vx_burn_unit, vy_burn_unit, vz_burn_unit;
            rotate(vx_earth_unit, vy_earth_unit, vz_earth_unit,
                   x_orbital_plane_unit, y_orbital_plane_unit, z_orbital_plane_unit,
                   &vx_burn_unit, &vy_burn_unit, &vz_burn_unit,
                   0);
            //double vx_burn = vx_burn_unit * burndvs[j] / UNIT_VELOCITY;
            //double vy_burn = vy_burn_unit * burndvs[j] / UNIT_VELOCITY;
            //double vz_burn = vz_burn_unit * burndvs[j] / UNIT_VELOCITY;
            double vx = (vx_earth_unit * e_speed +
                         vx_leo_unit * leo_speed +
                         vx_leo_unit * burndvs[j]) / UNIT_VELOCITY;
            double vy = (vy_earth_unit * e_speed +
                         vy_leo_unit * leo_speed +
                         vy_leo_unit * burndvs[j]) / UNIT_VELOCITY;

            double vz = (vz_earth_unit * e_speed +
                         vz_leo_unit * leo_speed +
                         vz_leo_unit * burndvs[j]) / UNIT_VELOCITY;
            double c_speed = UNIT_VELOCITY * sqrt(vx * vx + vy * vy + vz * vz);

            double vR_earth, vtheta_earth, vphi_earth;
            velocity_cartesian2spherical(x_earth, y_earth, z_earth, vx_earth, vy_earth, vz_earth, &vR_earth, &vtheta_earth, &vphi_earth);
            double R, theta, phi;
            cartesian2spherical(x, y, z, &R, &theta, &phi);
            double vR, vtheta, vphi;
            velocity_cartesian2spherical(x, y, z, vx, vy, vz, &vR, &vtheta, &vphi);
 
            double earth_distance = UNIT_LENGTH *
                distance(R, theta, phi, R_earth, theta_earth, phi_earth);
            /*
            printf("=========================== %i %i %i %i %.15f===============================\n", n, i, j, k, days[i]);
            printf("e_orbital_plane_cartesian=[%e %e %e]\n", x_orbital_plane_unit, y_orbital_plane_unit, z_orbital_plane_unit);
            printf("e_cartesian=[%f %f %f]\n", x_earth, y_earth, z_earth);
            printf("c_cartesian=[%f %f %f]\n", x, y, z);
            printf("c_e_distance=%f\n", earth_distance);
            printf("----------------------------------------------------\n");
            printf("tilt=%f\n", tilts[k]);
            printf("ev_cartesian=[%f %f %f]\n", vx_earth, vy_earth, vz_earth);
            printf("cv_cartesian=[%f %f %f]\n", vx, vy, vz);
            printf("ev_cartesian_unit=[%f %f %f]\n", vx_earth_unit, vy_earth_unit, vz_earth_unit);
            printf("c_leo_cartesian_unit=[%f %f %f]\n", x_leo_unit, y_leo_unit, z_leo_unit);
            printf("leo_cartesian_unit=[%f %f %f]\n", vx_leo_unit, vy_leo_unit, vz_leo_unit);
            printf("burn_cartesian_unit=[%f %f %f]\n", vx_burn_unit, vy_burn_unit, vz_burn_unit);
            printf("----------------------------------------------------\n");
            printf("e_speed=%f\n", e_speed);
            printf("leo_speed=%f\n", leo_speed);
            printf("burn_speed=%f\n", burn_speed);
            printf("c_speed=%f\n", c_speed);
            printf("----------------------------------------------------\n");
            printf("e_spherical=[%f %f %f]\n", R_earth, theta_earth, phi_earth);
            printf("c_spherical=[%f %f %f]\n", R, theta, phi);
            printf("ev_spherical=[%f %f %f]\n", vR_earth, vtheta_earth, vphi_earth);
            printf("cv_spherical=[%f %f %f]\n", vR, vtheta, vphi);
            printf("====================================================\n");
            */
            days_out[n] = days[i];
            Qs_out[3 * n + 0] = R;
            Qs_out[3 * n + 1] = theta;
            Qs_out[3 * n + 2] = phi;
            Bs_out[3 * n + 0] = get_B_R(vR);
            Bs_out[3 * n + 1] = get_B_theta(R, vtheta);
            Bs_out[3 * n + 2] = get_B_phi(R, theta, vphi);
        }
    }
} // extern "C"
