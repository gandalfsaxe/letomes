#pragma once

#include <math.h>

__host__ __device__
inline double get_Rdot(double B_R)
{
    return B_R;
}

__host__ __device__
inline double get_thetadot(double R, double B_theta)
{
    return B_theta / (R * R);
}

__host__ __device__
inline double get_phidot(double R, double theta, double B_phi)
{
    return B_phi / (R * R * sin(theta) * sin(theta));
}

__host__ __device__
inline double get_B_R(double Rdot)
{
    return Rdot;
}

__host__ __device__
inline double get_B_theta(double R, double thetadot)
{
    return R * R * thetadot;
}

__host__ __device__
inline double get_B_phi(double R, double theta, double phidot)
{
    return R * R * sin(theta) * sin(theta) * phidot;
}

__host__ __device__
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
    if (Bdot_R1 + Bdot_R2 + Bdot_R3 < -1e100)
    {
        printf("====== numerator_earth2=%.15le denominator_earth2=%.15le\n", numerator_earth2, denominator_earth2);
        printf("====== numerator_sun=%.15le numerator_earth=%.15le numerator_mars=%.15le\n", numerator_sun, numerator_earth, numerator_mars);
        printf("====== denominator_sun=%.15le denominator_earth=%.15le denominator_mars=%.15le\n", denominator_sun, denominator_earth, denominator_mars);
        printf("====== Bdot_R1=%.15lf Bdot_R2=%.15lf Bdot_R3=%.15lf\n", Bdot_R1, Bdot_R2, Bdot_R3);
    }
    */
    return Bdot_R1 + Bdot_R2 + Bdot_R3;
}

__host__ __device__
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

__host__ __device__
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
