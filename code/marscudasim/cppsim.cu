#include "constants.h"
#include "coordinate_system.h"
#include "euler_step.h"

#include <omp.h>
#include <cuda_runtime.h>
#include <helper_cuda.h>
#include <stdio.h>
#include <math.h>

#define M_2PI (2.0 * M_PI)
#define COND false //i % 1 == 0

extern "C" {

    void simulate_cpu(double h,
                      double max_duration,
                      int max_iter,
                      double* ts,
                      double* Rs, double* thetas, double* phis,
                      double* B_Rs, double* B_thetas, double* B_phis,
                      int size_ephemerides,
                      double* earth_R, double* earth_theta, double* earth_phi,
                      double* mars_R, double* mars_theta, double* mars_phi,
                      double* ts_out,
                      double* Qs_out,
                      int* i_final)
    {
        printf("cudasim::simulate_single(h=%.15le, max_duration=%.15le, max_iter=%i\n", h, max_duration, max_iter);
        double time = omp_get_wtime();
        printf("Running kernel: \n");

        const int pathNo = 0;
        double t = ts[pathNo];
        double R = Rs[pathNo];
        double theta = thetas[pathNo];
        double phi = phis[pathNo];
        double B_R = B_Rs[pathNo];
        double B_theta = B_thetas[pathNo];
        double B_phi = B_phis[pathNo];
        double Rdot = get_Rdot(B_R);
        double thetadot = get_thetadot(R, B_theta);
        double phidot = get_phidot(R, theta, B_phi);
        // ------ BEGIN SIMULATION ----
        max_duration += t;
        int i = 0;
        double sun_distance, earth_distance, mars_distance, mars_orbit;
        double min_mars_distance = 1e200, min_day = 0;
        double day;
        while (true)
        {
            ts_out[i] = t;
            Qs_out[i * 3 + 0] = R;
            Qs_out[i * 3 + 1] = theta;
            Qs_out[i * 3 + 2] = phi;

            //if (i % 1 == 0) printf("i=%i | t=%.15lf | h=%.15lf | R=%.15lf, theta=%.15lf, phi=%.15lf | B_R=%.15lf, B_theta=%.15lf, B_phi=%.15lf\n", i, t, h, R, theta, phi, B_R, B_theta, B_phi);
            day = t * UNIT_TIME / (3600.0 * 24.0);
            int idx = day;
            double d = day - idx;
            idx++;
            double R_sun = SUN_R;
            double theta_sun = SUN_THETA * M_PI / 180.0;
            double phi_sun = SUN_PHI;
            double R_earth = lerp(earth_R[idx], earth_R[idx + 1], d);
            double theta_earth = lerp(earth_theta[idx], earth_theta[idx + 1], d);
            double phi_earth = lerp(earth_phi[idx], earth_phi[idx + 1], d);
            double R_mars = lerp(mars_R[idx], mars_R[idx + 1], d);
            double theta_mars = lerp(mars_theta[idx], mars_theta[idx + 1], d);
            double phi_mars = lerp(mars_phi[idx], mars_phi[idx + 1], d);

            sun_distance = UNIT_LENGTH *
                distance(R, theta, phi, R_sun, theta_sun, phi_sun);
            earth_distance = UNIT_LENGTH *
                distance(R, theta, phi, R_earth, theta_earth, phi_earth);
            mars_distance = UNIT_LENGTH *
                distance(R, theta, phi, R_mars, theta_mars, phi_mars);
            mars_orbit = UNIT_LENGTH *
                distance(R_sun, theta_sun, phi_sun, R_mars, theta_mars, phi_mars);
            min_day = min_mars_distance > mars_distance ?
                day : min_day;
            min_mars_distance = min_mars_distance > mars_distance ?
                mars_distance : min_mars_distance;

            if (i == 0 || i % 100000 == 0)
            {
                printf("duration=%f i=%i pathNo=%i | R=%.15f theta=%.15f phi=%.15f | sun_dist=%i km earth_dist=%i km mars_dist=%i km mars_sun_dist=%i km | min_mars_dist=%i km\n",
                       (t - ts[pathNo]) * UNIT_TIME / (3600.0 * 24.0),
                       i, pathNo, R, theta, phi,
                       (int)sun_distance,
                       (int)earth_distance,
                       (int)mars_distance,
                       (int)mars_orbit,
                       (int)min_mars_distance);
            }
            if (t >= max_duration) {
                printf(".");
                i_final[pathNo] = i;
                break;
            }
            if (i >= max_iter) {
                printf("|");
                i_final[pathNo] = i;
                break;
            }
            /*
            if (earth_distance <= EARTH_RADIUS)
            {
                printf("o");
                i_final[pathNo] = i;
                break;
            }
            */
            if (sun_distance <= SUN_RADIUS)
            {
                printf("*");
                i_final[pathNo] = i;
                break;
            }
            if (mars_distance <= MARS_RADIUS)
            {
                printf("X");
                i_final[pathNo] = i;
                break;
            }
            /*
              if (mars_distance > min_mars_distance)
              {
              printf("-");
              i_final[pathNo] = day;
              score[pathNo] = min_mars_distance;
              break;
              }
            */

            euler_step(h, R, theta, phi, B_R, B_theta, B_phi,
                       R_sun, theta_sun, phi_sun,
                       R_earth, theta_earth, phi_earth,
                       R_mars, theta_mars, phi_mars,
                       &R, &theta, &phi, &B_R, &B_theta, &B_phi);
            t += h;
            i += 1;
        }
        printf("duration=%f i=%i pathNo=%i | R=%.15f theta=%.15f phi=%.15f | sun_dist=%i km earth_dist=%i km mars_dist=%i km mars_sun_dist=%i km | min_mars_dist=%i km\n",
               (t - ts[pathNo]) * UNIT_TIME / (3600.0 * 24.0),
               i, pathNo, R, theta, phi,
               (int)sun_distance,
               (int)earth_distance,
               (int)mars_distance,
               (int)mars_orbit,
               (int)min_mars_distance);
        printf("%6.4f seconds\n", omp_get_wtime() - time);
    }
} // extern "C"
