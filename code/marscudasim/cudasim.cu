#include "constants.h"
//#include "simulate.h"

#include <omp.h>
#include <cuda_runtime.h>
#include <helper_cuda.h>
#include <stdio.h>
#include <math.h>

//#define M_PI 3.14159265358979
#define M_2PI (2.0 * M_PI)

__device__
inline double get_Rdot(double B_R)
{
    return B_R;
}

__device__
inline double get_thetadot(double R, double B_theta)
{
    return B_theta / (R * R);
}

__device__
inline double get_phidot(double R, double theta, double B_phi)
{
    return B_phi / (R * R * sin(theta) * sin(theta));
}

__device__
inline double get_B_R(double Rdot)
{
    return Rdot;
}

__device__
inline double get_B_theta(double R, double thetadot)
{
    return R * R * thetadot;
}

__device__
inline double get_B_phi(double R, double theta, double phidot)
{
    return R * R * sin(theta) * sin(theta) * phidot;
}

__device__
inline double get_Bdot_R(double R, double theta, double phi, 
                         double B_theta, double B_phi,
                         double R_sun, double theta_sun, double phi_sun,
                         double R_earth, double theta_earth, double phi_earth,
                         double R_mars, double theta_mars, double phi_mars)
{
    double numerator_sun = SUN_ETA *
        (-R + R_sun * (cos(theta) * cos(theta_sun) + sin(theta) * sin(theta_sun) * cos(phi - phi_sun)));
    double denominator_sun = R * R + R_sun * R_sun -
        2.0 * R * R_sun * (cos(theta) * cos(theta_sun) +
                           sin(theta) * sin(theta_sun) * cos(phi - phi_sun));
    denominator_sun = denominator_sun * sqrt(denominator_sun);

    double numerator_earth = EARTH_ETA *
        (-R + R_earth * (cos(theta) * cos(theta_earth) + sin(theta) * sin(theta_earth) * cos(phi - phi_earth)));
    double denominator_earth = R * R + R_earth * R_earth -
        2.0 * R * R_earth * (cos(theta) * cos(theta_earth) +
                             sin(theta) * sin(theta_earth) * cos(phi - phi_earth));
    denominator_earth = denominator_earth * sqrt(denominator_earth);

    double numerator_mars = MARS_ETA *
        (-R + R_mars * (cos(theta) * cos(theta_mars) + sin(theta) * sin(theta_mars) * cos(phi - phi_mars)));
    double denominator_mars = R * R + R_mars * R_mars -
        2.0 * R * R_mars * (cos(theta) * cos(theta_mars) +
                            sin(theta) * sin(theta_mars) * cos(phi - phi_mars));
    denominator_mars = denominator_mars * sqrt(denominator_mars);
    double Bdot_R1 = (B_theta * B_theta) / (R * R * R);
    double Bdot_R2 = (B_phi * B_phi) /(R * R * R * sin(theta) * sin(theta));
    double Bdot_R3 =
        (numerator_sun / denominator_sun) +
        (numerator_earth / denominator_earth) +
        (numerator_mars / denominator_mars);
    /*
    printf("====== numerator_sun=%.15le numerator_earth=%.15le numerator_mars=%.15le\n", numerator_sun, numerator_earth, numerator_mars);
    printf("====== denominator_sun=%.15le denominator_earth=%.15le denominator_mars=%.15le\n", denominator_sun, denominator_earth, denominator_mars);
    printf("====== Bdot_R1=%.15lf Bdot_R2=%.15lf Bdot_R3=%.15lf\n", Bdot_R1, Bdot_R2, Bdot_R3);
    */
    return Bdot_R1 + Bdot_R2 + Bdot_R3;
}

__device__
inline double get_Bdot_theta(double R, double theta, double phi, 
                             double B_phi,
                             double R_sun, double theta_sun, double phi_sun,
                             double R_earth, double theta_earth, double phi_earth,
                             double R_mars, double theta_mars, double phi_mars)
{
    double numerator_sun = SUN_ETA * 
        (R * R_sun * (-sin(theta) * cos(theta_sun) + cos(theta) * sin(theta_sun) * cos(phi - phi_sun)));
    double denominator_sun = R * R + R_sun * R_sun -
        2.0 * R * R_sun * (cos(theta) * cos(theta_sun) +
                           sin(theta) * sin(theta_sun) * cos(phi - phi_sun));
    denominator_sun = denominator_sun * sqrt(denominator_sun);
    double numerator_earth = EARTH_ETA * 
        (R * R_earth * (-sin(theta) * cos(theta_earth) + cos(theta) * sin(theta_earth) * cos(phi - phi_earth)));
    double denominator_earth = R * R + R_earth * R_earth -
        2.0 * R * R_earth * (cos(theta) * cos(theta_earth) +
                           sin(theta) * sin(theta_earth) * cos(phi - phi_earth));
    denominator_earth = denominator_earth * sqrt(denominator_earth);
    double numerator_mars = MARS_ETA * 
        (R * R_mars * (-sin(theta) * cos(theta_mars) + cos(theta) * sin(theta_mars) * cos(phi - phi_mars)));
    double denominator_mars = R * R + R_mars * R_mars -
        2.0 * R * R_mars * (cos(theta) * cos(theta_mars) +
                           sin(theta) * sin(theta_mars) * cos(phi - phi_mars));
    denominator_mars = denominator_mars * sqrt(denominator_mars);

    double Bdot_theta1 = (B_phi * B_phi) /
        (R * R * sin(theta) * sin(theta) * tan(theta));
    double Bdot_theta2 =
        numerator_sun / denominator_sun + 
        numerator_earth / denominator_earth + 
        numerator_mars / denominator_mars;
    return Bdot_theta1 + Bdot_theta2;
}

__device__
inline double get_Bdot_phi(double R, double theta, double phi, 
                           double R_sun, double theta_sun, double phi_sun,
                           double R_earth, double theta_earth, double phi_earth,
                           double R_mars, double theta_mars, double phi_mars)
{
    double numerator_sun = SUN_ETA * 
        (-R * R_sun * sin(theta) * sin(theta_sun) * sin(phi - phi_sun));
    double denominator_sun = R * R + R_sun * R_sun -
        2.0 * R * R_sun * (cos(theta) * cos(theta_sun) +
                           sin(theta) * sin(theta_sun) * cos(phi - phi_sun));
    denominator_sun = denominator_sun * sqrt(denominator_sun);
    double numerator_earth = EARTH_ETA * 
        (-R * R_earth * sin(theta) * sin(theta_earth) * sin(phi - phi_earth));
    double denominator_earth = R * R + R_earth * R_earth -
        2.0 * R * R_earth * (cos(theta) * cos(theta_earth) +
                           sin(theta) * sin(theta_earth) * cos(phi - phi_earth));
    denominator_earth = denominator_earth * sqrt(denominator_earth);
    double numerator_mars = MARS_ETA * 
        (-R * R_mars * sin(theta) * sin(theta_mars) * sin(phi - phi_mars));
    double denominator_mars = R * R + R_mars * R_mars -
        2.0 * R * R_mars * (cos(theta) * cos(theta_mars) +
                           sin(theta) * sin(theta_mars) * cos(phi - phi_mars));
    denominator_mars = denominator_mars * sqrt(denominator_mars);
    return
        numerator_sun / denominator_sun + 
        numerator_earth / denominator_earth + 
        numerator_mars / denominator_mars;
}

__device__
inline double keep_theta_in_interval_zero_to_pi(double theta)
{
    theta = fmod(theta,  M_2PI);
    return theta > M_PI ? M_2PI - theta : theta;
}

__device__
inline double keep_phi_in_interval_npi_to_pi(double phi)
{
    phi = fmod(phi, M_2PI);
    return phi > M_PI ? phi - M_2PI : phi;
}

__device__
inline double lerp(double v0, double v1, double t)
{
    return (1 - t) * v0 + t * v1;
    //return v0 + t * (v1 - v0);
}

extern "C" {


    // ----------------- MAIN ALGORITHM ----------------------------
    // explicit euler algorithm for 4-body case
    // All values are with nondimensionalized units
    __global__
    void simulate_kernel(int number_of_paths,
                         double fan_delta,
                         int coordinate_no,
                         double h,
                         double max_duration,
                         int max_iter,
                         double t,
                         double R, double theta, double phi,
                         double B_R, double B_theta, double B_phi,
                         double* earth_R, double* earth_theta, double* earth_phi,
                         double* mars_R, double* mars_theta, double* mars_phi,
                         bool* success,
                         double* score)
    {
        const int pathNo = blockIdx.x * blockDim.x + threadIdx.x;
        if (pathNo < number_of_paths)
        {
            // Implement simple fan search.
            double dB = (fan_delta / number_of_paths) * pathNo -0.5 * fan_delta;
            B_R = coordinate_no == 0 ? B_R + dB : B_R;
            B_theta = coordinate_no == 1 ? B_theta + dB : B_theta;
            B_phi = coordinate_no == 2 ? B_phi + dB : B_phi;

            // ------ BEGIN SIMULATION ----
            int i = 0;
            while (true)
            {
                //if (i % 1000 == 0) printf("i=%i | t=%.15lf | h=%.15lf | R=%.15lf, theta=%.15lf, phi=%.15lf | B_R=%.15lf, B_theta=%.15lf, B_phi=%.15lf\n", i, t, h, R, theta, phi, B_R, B_theta, B_phi);
                i += 1;
                t += h;

                double day = t * UNIT_TIME / (3600.0 * 24.0);
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
                //printf("R_sun=%.15lf, theta_sun=%.15lf, phi_sun=%.15lf\n", R_sun, theta_sun, phi_sun);
                //printf("R_earth=%.15lf, theta_earth=%.15lf, phi_earth=%.15lf\n", R_earth, theta_earth, phi_earth);
                //printf("R_mars=%.15lf, theta_mars=%.15lf, phi_mars=%.15lf\n", R_mars, theta_mars, phi_mars);

                // Update q
                R = R + h * get_Rdot(B_R);
                theta = theta + h * get_thetadot(R, B_theta);
                phi = phi + h * get_phidot(R, theta, B_phi);
                theta = keep_theta_in_interval_zero_to_pi(theta);
                phi = keep_phi_in_interval_npi_to_pi(phi);

                // Update B_R
                B_R += h * get_Bdot_R(R, theta, phi,
                                      B_theta, B_phi,
                                      R_sun, theta_sun, phi_sun,
                                      R_earth, theta_earth, phi_earth,
                                      R_mars, theta_mars, phi_mars);
                // Update B_theta
                B_theta += h * get_Bdot_theta(R, theta, phi,
                                              B_phi,
                                              R_sun, theta_sun, phi_sun,
                                              R_earth, theta_earth, phi_earth,
                                              R_mars, theta_mars, phi_mars);
                // Update B_phi
                B_phi += h * get_Bdot_phi(R, theta, phi,
                                          R_sun, theta_sun, phi_sun,
                                          R_earth, theta_earth, phi_earth,
                                          R_mars, theta_mars, phi_mars);

                if (t >= max_duration) {
                    printf(".");
                    success[pathNo] = false;
                    return;
                }
                if (i >= max_iter) {
                    printf("|");
                    success[pathNo] = false;
                    return;
                }
            }
            printf("X");
            score[pathNo] = 100;
            success[pathNo] = true;
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
                  double fan_delta,
                  int coordinate_no,
                  double h,
                  double max_duration,
                  int max_iter,
                  double t,
                  double* Q,
                  double* B,
                  int size_ephemerides,
                  double* earth_R, double* earth_theta, double* earth_phi,
                  double* mars_R, double* mars_theta, double* mars_phi,
                  bool* success,
                  double* score)
    {
        printf("cudasim::simulate(number_of_paths=%i, fan_delta=%.15le, coordinate_no=%i, h=%.15le, max_duration=%.15le, max_iter=%i, t=%.15le, Q=[%f,%f,%f], B=[%f,%f,%f]\n", number_of_paths, fan_delta, coordinate_no, h, max_duration, max_iter, t, Q[0], Q[1], Q[2], B[0], B[1], B[2]);

        // Warm up..
        const int devNo = 1;
        deviceQuery(devNo);
        deviceWarmup(devNo);

        // Allocate memory.
        double time = omp_get_wtime();
        printf("Allocate memory + transfer ephemerides: ");
        const int nBytesScore = number_of_paths * sizeof(double);
        const int nBytesSuccess = number_of_paths * sizeof(bool);
        const int nBytesEphemerides = size_ephemerides * sizeof(double);
        bool* success_d;
        double* score_d;
        double* earth_R_d;
        double* earth_theta_d;
        double* earth_phi_d;
        double* mars_R_d;
        double* mars_theta_d;
        double* mars_phi_d;
        checkCudaErrors(cudaMalloc((void**)&earth_R_d, nBytesEphemerides));
        checkCudaErrors(cudaMalloc((void**)&earth_theta_d, nBytesEphemerides));
        checkCudaErrors(cudaMalloc((void**)&earth_phi_d, nBytesEphemerides));
        checkCudaErrors(cudaMalloc((void**)&mars_R_d, nBytesEphemerides));
        checkCudaErrors(cudaMalloc((void**)&mars_theta_d, nBytesEphemerides));
        checkCudaErrors(cudaMalloc((void**)&mars_phi_d, nBytesEphemerides));
        checkCudaErrors(cudaMalloc((void**)&success_d, nBytesSuccess));
        checkCudaErrors(cudaMalloc((void**)&score_d, nBytesScore));
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
        dim3 block(256);
        dim3 grid((number_of_paths - 1) / block.x + 1);
        simulate_kernel<<<grid, block>>>(number_of_paths,
                                         fan_delta,
                                         coordinate_no,
                                         h,
                                         max_duration,
                                         max_iter,
                                         t,
                                         Q[0], Q[1], Q[2],
                                         B[0], B[1], B[2],
                                         earth_R_d, earth_theta_d, earth_phi_d,
                                         mars_R_d, mars_theta_d, mars_phi_d,
                                         success_d,
                                         score_d);
        checkCudaErrors(cudaDeviceSynchronize());
        printf("%6.4f seconds\n", omp_get_wtime() - time);

        // Copy results.
        time = omp_get_wtime();
        printf("Transfering result (%i KiB): ", (nBytesSuccess + nBytesScore) / 1024);
        checkCudaErrors(cudaMemcpy(success,
                                   success_d,
                                   nBytesSuccess,
                                   cudaMemcpyDeviceToHost));
        checkCudaErrors(cudaMemcpy(score,
                                   score_d,
                                   nBytesScore,
                                   cudaMemcpyDeviceToHost));
        printf("%6.4f seconds\n", omp_get_wtime() - time);

        // Clean up.
        checkCudaErrors(cudaFree(success_d));
        checkCudaErrors(cudaFree(score_d));
    }

} // extern "C"
