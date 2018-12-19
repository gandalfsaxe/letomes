#include "constants.h"
#include "coordinate_system.h"
#include "equations_of_motion.h"

#include <omp.h>
#include <cuda_runtime.h>
#include <helper_cuda.h>
#include <stdio.h>
#include <math.h>

#define M_2PI (2.0 * M_PI)
#define COND false //i % 1 == 0

#include "euler_step.h"

extern "C" {

    __global__
    void simulate_kernel(int number_of_paths,
                         double h,
                         double max_duration,
                         int max_iter,
                         double* ts,
                         double* Rs, double* thetas, double* phis,
                         double* B_Rs, double* B_thetas, double* B_phis,
                         double* earth_R, double* earth_theta, double* earth_phi,
                         double* mars_R, double* mars_theta, double* mars_phi,
                         double* arive,
                         double* score)
    {
        const int pathNo = blockIdx.x * blockDim.x + threadIdx.x;
        if (pathNo < number_of_paths)
        {
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
            //printf("pathNo=%i t=%.15e | R, theta, phi = [%.15e, %.15e, %.15e], B_R, B_theta, B_pi = [%.15e, %.15e, %.15e], Rdot, thetadot, pidot = [%.15e, %.15e, %.15e]\n", pathNo, t, R, theta, phi, B_R, B_theta, B_phi, Rdot, thetadot, phidot);
            // ------ BEGIN SIMULATION ----
            max_duration += t;
            int i = 0;
            double sun_distance, earth_distance, mars_distance, mars_orbit;
            double min_mars_distance = 1e200, min_day = 0;
            double day;
            while (true)
            {
                //if (COND) printf("i=%i | t=%.15lf | h=%.15lf | R=%.15lf, theta=%.15lf, phi=%.15lf | B_R=%.15lf, B_theta=%.15lf, B_phi=%.15lf\n", i, t, h, R, theta, phi, B_R, B_theta, B_phi);
                day = t * UNIT_TIME / (3600.0 * 24.0);
                int idx = day;
                double d = day - idx;
                idx++;
                double R_sun = SUN_R, theta_sun = SUN_THETA * M_PI / 180.0, phi_sun = SUN_PHI;
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
                if (false && i == 0)
                {
                    const char inside[] = "<=";
                    const char outside[] = "=>";
                    const char* away = sun_distance < mars_orbit ? inside : outside;
                    printf("duration=%f i=%i pathNo=%i | R=%.15f theta=%.15f phi=%.15f | sun_dist=%i km earth_dist=%i km mars_dist=%i km | mars_orbit=%i km %s\n",
                           (t - ts[pathNo]) * UNIT_TIME / (3600.0 * 24.0),
                           i, pathNo, R, theta, phi,
                           (int)sun_distance,
                           (int)earth_distance,
                           (int)mars_distance,
                           (int)mars_orbit,
                           away);
                    //printf("day=%.15e idx=%i d=%.15e\n", day, idx, d);
                    //printf("R_sun=%.15lf, theta_sun=%.15lf, phi_sun=%.15lf\n", R_sun, theta_sun, phi_sun);
                    //printf("R_earth=%.15lf, theta_earth=%.15lf, phi_earth=%.15lf\n", R_earth, theta_earth, phi_earth);
                    //printf("R_mars=%.15lf, theta_mars=%.15lf, phi_mars=%.15lf\n", R_mars, theta_mars, phi_mars);
                }
                if (t >= max_duration) {
                    printf(".");
                    arive[pathNo] = min_day;
                    score[pathNo] = min_mars_distance;
                    break;
                }
                if (i >= max_iter) {
                    printf("|");
                    arive[pathNo] = min_day;
                    score[pathNo] = min_mars_distance;
                    break;
                }
                if (sun_distance <= SUN_RADIUS)
                {
                    printf("*");
                    arive[pathNo] = min_day;
                    score[pathNo] = min_mars_distance;
                    break;
                }
                if (earth_distance <= EARTH_RADIUS)
                {
                    printf("o");
                    arive[pathNo] = min_day;
                    score[pathNo] = min_mars_distance;
                    break;
                }
                if (mars_distance <= MARS_RADIUS)
                {
                    printf("X");
                    arive[pathNo] = min_day;
                    score[pathNo] = 0;
                    break;
                }
                /*
                if (mars_distance > min_mars_distance)
                {
                    printf("-");
                    arive[pathNo] = day;
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
            /*
            const char inside[] = "<=";
            const char outside[] = "=>";
            const char* away = sun_distance < mars_orbit ? inside : outside;
            printf("END: duration=%f i=%i pathNo=%i | R=%.15f theta=%.15f phi=%.15f | sun_dist=%i km earth_dist=%i km mars_dist=%i km | mars_orbit=%i km min_mars_dist=%i km %s\n",
                   (t - ts[pathNo]) * UNIT_TIME / (3600.0 * 24.0),
                   i, pathNo, R, theta, phi,
                   (int)sun_distance,
                   (int)earth_distance,
                   (int)mars_distance,
                   (int)mars_orbit,
                   (int)min_mars_distance,
                   away);
            */
        }
    }

    void deviceQuery(int devNo)
    {
        cudaDeviceProp prop;
        cudaGetDeviceProperties(&prop, devNo);
        printf("Device %i: \"%s\".\n", devNo, prop.name);
        int nProcessors = prop.multiProcessorCount;
        int nCores = _ConvertSMVer2Cores(prop.major, prop.minor) * nProcessors;
        int clockFreq = prop.clockRate / 1000;
        int peakPerformanceSP = round(2.0e-3 * clockFreq * nCores);
        int singleToDoubleRatio = prop.singleToDoublePrecisionPerfRatio;
        int peakPerformanceDP = peakPerformanceSP / singleToDoubleRatio;
        int peakBandwidth = round(2.0 * prop.memoryClockRate * 1e-6 *
                                  (prop.memoryBusWidth / 8));
        printf("  Multiprocessors:  %6i\n", nProcessors);
        printf("  Cores:            %6i\n", nCores);
        printf("  Peak performance: %6i GFlops\n", peakPerformanceDP);
        printf("  Peak bandwidth:   %6i GB/s\n", peakBandwidth);
    }

    void deviceWarmup(int devNo)
    {
        printf("Warming up device: "); fflush(stdout);
        double time = omp_get_wtime();
        cudaSetDevice(devNo);
        double *dummy_d;
        cudaMalloc((void**)&dummy_d, 0); // We force the creation of context on
                                         // the device by allocating a dummy.
        printf("%6.4f seconds\n", omp_get_wtime() - time);
    }

    void simulate(int number_of_paths,
                  double h,
                  double max_duration,
                  int max_iter,
                  double* t,
                  double* R, double* theta, double* phi,
                  double* B_R, double* B_theta, double* B_phi,
                  int size_ephemerides,
                  double* earth_R, double* earth_theta, double* earth_phi,
                  double* mars_R, double* mars_theta, double* mars_phi,
                  double* arive,
                  double* score)
    {
        printf("cudasim::simulate(number_of_paths=%i, h=%.15le, max_duration=%.15le, max_iter=%i\n", number_of_paths, h, max_duration, max_iter);

        // Warm up..
        const int devNo = 0;
        deviceQuery(devNo);
        deviceWarmup(devNo);

        // Allocate memory.
        double time = omp_get_wtime();
        printf("Allocate memory + transfer ephemerides: ");
        const int nBytes = number_of_paths * sizeof(double);
        const int nBytesArive = number_of_paths * sizeof(double);
        const int nBytesEphemerides = size_ephemerides * sizeof(double);
        double* t_d;
        double* R_d;
        double* theta_d;
        double* phi_d;
        double* B_R_d;
        double* B_theta_d;
        double* B_phi_d;
        double* arive_d;
        double* score_d;
        double* earth_R_d;
        double* earth_theta_d;
        double* earth_phi_d;
        double* mars_R_d;
        double* mars_theta_d;
        double* mars_phi_d;
        checkCudaErrors(cudaMalloc((void**)&t_d, nBytes));
        checkCudaErrors(cudaMalloc((void**)&R_d, nBytes));
        checkCudaErrors(cudaMalloc((void**)&theta_d, nBytes));
        checkCudaErrors(cudaMalloc((void**)&phi_d, nBytes));
        checkCudaErrors(cudaMalloc((void**)&B_R_d, nBytes));
        checkCudaErrors(cudaMalloc((void**)&B_theta_d, nBytes));
        checkCudaErrors(cudaMalloc((void**)&B_phi_d, nBytes));
        checkCudaErrors(cudaMalloc((void**)&earth_R_d, nBytesEphemerides));
        checkCudaErrors(cudaMalloc((void**)&earth_theta_d, nBytesEphemerides));
        checkCudaErrors(cudaMalloc((void**)&earth_phi_d, nBytesEphemerides));
        checkCudaErrors(cudaMalloc((void**)&mars_R_d, nBytesEphemerides));
        checkCudaErrors(cudaMalloc((void**)&mars_theta_d, nBytesEphemerides));
        checkCudaErrors(cudaMalloc((void**)&mars_phi_d, nBytesEphemerides));
        checkCudaErrors(cudaMalloc((void**)&arive_d, nBytesArive));
        checkCudaErrors(cudaMalloc((void**)&score_d, nBytes));
        checkCudaErrors(cudaMemcpy(t_d,
                                   t,
                                   nBytes,
                                   cudaMemcpyHostToDevice));
        checkCudaErrors(cudaMemcpy(R_d,
                                   R,
                                   nBytes,
                                   cudaMemcpyHostToDevice));
        checkCudaErrors(cudaMemcpy(theta_d,
                                   theta,
                                   nBytes,
                                   cudaMemcpyHostToDevice));
        checkCudaErrors(cudaMemcpy(phi_d,
                                   phi,
                                   nBytes,
                                   cudaMemcpyHostToDevice));
        checkCudaErrors(cudaMemcpy(B_R_d,
                                   B_R,
                                   nBytes,
                                   cudaMemcpyHostToDevice));
        checkCudaErrors(cudaMemcpy(B_theta_d,
                                   B_theta,
                                   nBytes,
                                   cudaMemcpyHostToDevice));
        checkCudaErrors(cudaMemcpy(B_phi_d,
                                   B_phi,
                                   nBytes,
                                   cudaMemcpyHostToDevice));
        checkCudaErrors(cudaMemcpy(earth_R_d,
                                   earth_R,
                                   nBytesEphemerides,
                                   cudaMemcpyHostToDevice));
        checkCudaErrors(cudaMemcpy(earth_theta_d,
                                   earth_theta,
                                   nBytesEphemerides,
                                   cudaMemcpyHostToDevice));
        checkCudaErrors(cudaMemcpy(earth_phi_d,
                                   earth_phi,
                                   nBytesEphemerides,
                                   cudaMemcpyHostToDevice));
        checkCudaErrors(cudaMemcpy(mars_R_d,
                                   mars_R,
                                   nBytesEphemerides,
                                   cudaMemcpyHostToDevice));
        checkCudaErrors(cudaMemcpy(mars_theta_d,
                                   mars_theta,
                                   nBytesEphemerides,
                                   cudaMemcpyHostToDevice));
        checkCudaErrors(cudaMemcpy(mars_phi_d,
                                   mars_phi,
                                   nBytesEphemerides,
                                   cudaMemcpyHostToDevice));
        printf("%6.4f seconds\n", omp_get_wtime() - time);

        // Launch kernel.
        time = omp_get_wtime();
        printf("Running kernel: \n");
        dim3 block(160);
        dim3 grid((number_of_paths - 1) / block.x + 1);
        simulate_kernel<<<grid, block>>>(number_of_paths,
                                         h,
                                         max_duration,
                                         max_iter,
                                         t_d,
                                         R_d, theta_d, phi_d,
                                         B_R_d, B_theta_d, B_phi_d,
                                         earth_R_d, earth_theta_d, earth_phi_d,
                                         mars_R_d, mars_theta_d, mars_phi_d,
                                         arive_d,
                                         score_d);
        checkCudaErrors(cudaDeviceSynchronize());
        printf("%6.4f seconds\n", omp_get_wtime() - time);

        // Copy results.
        time = omp_get_wtime();
        printf("Transfering result (%i KiB): ", (nBytesArive + nBytes) / 1024);
        checkCudaErrors(cudaMemcpy(arive,
                                   arive_d,
                                   nBytesArive,
                                   cudaMemcpyDeviceToHost));
        checkCudaErrors(cudaMemcpy(score,
                                   score_d,
                                   nBytes,
                                   cudaMemcpyDeviceToHost));
        printf("%6.4f seconds\n", omp_get_wtime() - time);

        // Clean up.
        checkCudaErrors(cudaFree(arive_d));
        checkCudaErrors(cudaFree(score_d));
    }

} // extern "C"
