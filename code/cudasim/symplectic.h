#pragma once

#include <cuda_runtime.h>

__device__
void symplectic(double x0,
                double y0,
                double p0_x,
                double p0_y,
                double maxDuration,
                double maxIter,
                double* score,
                bool* success);
