#include <omp.h>
#include <cuda_runtime.h>
#include <helper_cuda.h>
#include <stdio.h>
#include <math.h>

#include "constants.h"
#include "simulate.h"

extern "C" {

    __global__
    void kernel(int nTrajectories,
                psitype* psis,
                bool* successes,
                double* scores)
    {
        const int trajIdx = blockIdx.x * blockDim.x + threadIdx.x;
        
        if trajIdx < nTrajectories //for each path
        {
            psitype* thisPsi = psis[sizeof(psitype) * trajIdx];
            simulate(thisPsi, &successes[trajIdx], &scores[trajIdx]);
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
        printf("Warming up device... "); fflush(stdout);
        double time = omp_get_wtime();
        cudaSetDevice(devNo);
        double *dummy_d;
        cudaMalloc((void**)&dummy_d, 0); // We force the creation of context on
                                         // the device by allocating a dummy.
        printf("%6.4f seconds\n", omp_get_wtime() - time);
    }

    // launch (not really a launch since we start from LEO) a 
    // single rocket with a given set of hyperparameters, return the path
    __global__
    void oldkernel(int nPaths,
                double maxDuration,
                int maxSteps,
                double* points,
                bool* success,
                double* score)
    {
        const int pathNo = blockIdx.x * blockDim.x + threadIdx.x;

        if (pathNo < nPaths)
        {
            double posAng = points[3 * pathNo + 0];
            double burnAng = points[3 * pathNo + 1];
            double burnDv = points[3 * pathNo + 2];

            maxDuration /= UNIT_TIME;

            // position (where on earth do we start our burn)
            double x0 = cos(posAng) * LEO_RADIUS_NONDIM;
            double y0 = sin(posAng) * LEO_RADIUS_NONDIM;
            x0 += EARTH_POSITION_X;

            // how fast are we going when we start?
            double vhat_x = -sin(posAng);
            double vhat_y = cos(posAng);
            double v_x = LEO_VELOCITY_NONDIM * vhat_x;
            double v_y = LEO_VELOCITY_NONDIM * vhat_y;

            // burn vector: At what angle do we launch outward, and how hard do we push?
            double burnDv_x = cos(burnAng) * vhat_x - sin(burnAng) * vhat_y;
            double burnDv_y = sin(burnAng) * vhat_x + cos(burnAng) * vhat_y;

            // resultant momentum vector
            double p0_x = v_x + burnDv * burnDv_x / UNIT_VELOCITY - y0;
            double p0_y = v_y + burnDv * burnDv_y / UNIT_VELOCITY + x0;

            // SIMULATE
            //printf("pathNo = %i | posAng = %.15lf, burnAng = %.15lf, burnDv = %.15lf: running symplectic with [x0, y0, p0_x, p0_y] = {%.15lf, %.15lf, %.15lf, %.15lf}\n", pathNo, posAng, burnAng, burnDv, x0, y0, p0_x, p0_y);
            symplectic(x0,
                       y0,
                       p0_x,
                       p0_y,
                       maxDuration,
                       maxSteps,
                       &score[pathNo],
                       &success[pathNo]);
        }
    }

    void integrate(int nIndividuals,
                   int nJitter,
                   double maxDuration,
                   int maxSteps,
                   double* points,
                   bool* success,
                   double* score
                   )
    {
        const int devNo = 1;

        deviceQuery(devNo);
        deviceWarmup(devNo);

        // Allocate array on device and transfer input.
        bool* success_d; double* points_d, * score_d;
        const int nPaths = nIndividuals * nJitter;
        const int nBytesPath = nPaths * 3 * sizeof(double);
        const int nBytesSuccess = nPaths * sizeof(bool);
        const int nBytesScore = nPaths * sizeof(double);
        const int nBytes = nBytesPath + nBytesSuccess + nBytesScore;
        double time = omp_get_wtime();
        printf("Transfering input (%i KiB)... ", nBytes / 1024);
        checkCudaErrors(cudaMalloc((void**)&points_d, nBytesPath));
        checkCudaErrors(cudaMalloc((void**)&success_d, nBytesSuccess));
        checkCudaErrors(cudaMalloc((void**)&score_d, nBytesScore));
        checkCudaErrors(cudaMemcpy(points_d,
                                   points,
                                   nBytesPath,
                                   cudaMemcpyHostToDevice));
        printf("%6.4f seconds\n", omp_get_wtime() - time);

        // Launch kernel.
        time = omp_get_wtime();
        printf("Running kernel... ");
        dim3 block(256);
        dim3 grid((nPaths - 1) / block.x + 1);
        kernel<<<grid, block>>>(nPaths, maxDuration, maxSteps, points_d, success_d, score_d);
        checkCudaErrors(cudaDeviceSynchronize());
        printf("%6.4f seconds\n", omp_get_wtime() - time);

        time = omp_get_wtime();
        printf("Transfering result (%i KiB)... ", (nBytesSuccess + nBytesScore) / 1024);
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
        checkCudaErrors(cudaFree(points_d));
        checkCudaErrors(cudaFree(success_d));
        checkCudaErrors(cudaFree(score_d));
    }
}
