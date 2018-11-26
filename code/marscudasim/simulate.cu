#include <omp.h>
#include <cuda_runtime.h>
#include <helper_cuda.h>
#include <stdio.h>
#include <math.h>

#include "simulate.h"
#include "constants.h"



__device__
inline double get_B_phi(double R, double theta, double phidot)
{
    return R * R * sin(theta) * sin(theta) * phidot;
}

__device__
inline double get_B_theta(double R, double thetadot)
{
    return R * R * thetadot;
}

// from position and momentum vectors, returns generalized momentum, nondimensionalized
__device__
inline double get_B_R(double Rdot)
{
    return Rdot;
}

__device__
inline double get_Bdot_phi(double R, double theta, double phi, double* R_ks, double* theta_ks, double* phi_ks)
{
    return 0 //TODO: implement. it's a bit hairy.;
}

__device__
inline double get_Bdot_theta(double R, double theta, double phi, double B_phi, double* R_ks, double* theta_ks, double* phi_ks)
{
    return 0 //TODO: implement ;
}

__device__
inline double get_Bdot_R(double R, double theta, double phi, double B_theta, double B_phi, double* R_ks, double* theta_ks, double* phi_ks)
{
    return 0 //TODO: implement ;
}

__device__
inline double get_Rdot(double B_R):
{
    return B_R;
}

__device__
inline double get_thetadot(double R, double B_theta):
{
    return B_theta / (R * R);
}

__device__
inline double get_phidot(double R, double theta, double B_phi):
{
    return B_phi / (R * R * sin(theta) * sin(theta));
}

double * get_ephemerides_on_day(double * ephemerides, int ephsize, double day_idx){
    /*  input:
            per-day ephemerides for a given body, 
            the size of the coordinate set (column count, basically),
            and the non-integer day you want to interpolate on.
        output: 
            a list of interpolated coordinates for the given day
    */ 
    double day = day_idx + 1;

    int day_lb = int(floor(day));
    int day_ub = int(ceil(day));
    double day_diff = day % 1;

    double * lowerbound_eph = ephemerides[day_lb*ephsize]; // maybe needs sizeof(double) in the index??
    double * upperbound_eph = ephemerides[day_ub*ephsize]; // maybe needs sizeof(double) in the index??
    double result[ephsize] = 
    for(int i = 0; i < ephsize; i++){
        double lb_val = lowerbound_eph[i];
        double ub_val = upperbound_eph[i];

        double diff_val = ub_val - lb_val;
        result[i] = lb_val + diff_val * day_diff;
    }   
    return result;
}

// ----------------- MAIN ALGORITHM ----------------------------
// explicit euler algorithm for 4-body case
// All values are with nondimensionalized units
__device__
void simulate(psitype* psi,
                double h, // timestep
                double* score, 
                bool* success,
                int max_duration,
                int max_iter)
{
    // Unpack psi
    t = psi.t;
    Q = psi.Q;
    B = psi.B;
    burn = psi.burn;

    day = t* UNIT_TIME / (3600 * 24);

    ephemerides = get_ephemerides(max_year); //TODO: implement get_ephemerides for C

    R = Q[0];
    theta = Q[1];
    phi = Q[2];

    B_R = B[0];
    B_theta = B[1];
    B_phi = B[2];


    // ------ BEGIN SIMULATION ----
    i = 0;
    while(true)
    {
        i += 1;
        t += h;
        day = t * UNIT_TIME / (3600 * 24);

        eph_on_day = get_ephemerides_on_day(ephemerides, day);
        eph_coords = get_ephemerides_on_day_rad(ephemerides, day);

        euler_sym = euler_step_symplectic(h,Q,B,eph_coords);
        Q = euler_sym[0];
        B = euler_sym[1];

        if(t >= max_duration){
            print(".");
            break;
        }
        if( i >= max_iter){
            print('|');
            break;
        }
        if(false){
            // TODO: success handling
        }
    }
    score[0] = 100
    success[0] = false
}
