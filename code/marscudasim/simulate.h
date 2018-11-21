#pragma once

#include <cuda_runtime.h>

typedef struct {
    double t;
    double Q0[3];
    double B0[3];
    double burn;
} psitype;

__device__
void simulate(psitype* psi,
                double* score,
                bool* success);
