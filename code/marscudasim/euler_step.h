#pragma once

#include "equations_of_motion.h"

__host__ __device__
inline void euler_step(double h,
                       double R, double theta, double phi,
                       double B_R, double B_theta, double B_phi,
                       double R_sun, double theta_sun, double phi_sun,
                       double R_earth, double theta_earth, double phi_earth,
                       double R_mars, double theta_mars, double phi_mars,
                       double* R_, double* theta_, double* phi_,
                       double* B_R_, double* B_theta_, double* B_phi_)
{
    // Update q
    R = R + h * get_Rdot(B_R);
    theta = theta + h * get_thetadot(R, B_theta);
    phi = phi + h * get_phidot(R, theta, B_phi);
    *R_ = R;
    *theta_ = theta;
    *phi_ = phi;

    // Update B_R
    *B_R_ = B_R + h * get_Bdot_R(R, theta, phi,
                                 B_theta, B_phi,
                                 R_sun, theta_sun, phi_sun,
                                 R_earth, theta_earth, phi_earth,
                                 R_mars, theta_mars, phi_mars);
    // Update B_theta
    *B_theta_ = B_theta + h * get_Bdot_theta(R, theta, phi,
                                             B_phi,
                                             R_sun, theta_sun, phi_sun,
                                             R_earth, theta_earth, phi_earth,
                                             R_mars, theta_mars, phi_mars);
    // Update B_phi
    *B_phi_ = B_phi + h * get_Bdot_phi(R, theta, phi,
                                       R_sun, theta_sun, phi_sun,
                                       R_earth, theta_earth, phi_earth,
                                       R_mars, theta_mars, phi_mars);
}
