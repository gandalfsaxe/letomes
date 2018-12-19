#pragma once

#include <math.h>

__host__ __device__
inline void rotate(double vx, double vy, double vz,
                   double kx, double ky, double kz,
                   double* x, double* y, double* z,
                   double theta)
{
    double cos_theta = cos(theta);
    double sin_theta = sin(theta);
    double cx = ky * vz - kz * vy;
    double cy = kz * vx - kx * vz;
    double cz = kx * vy - ky * vx;
    double d = vx * kx + vy * ky + vz * kz;
    *x = vx * cos_theta + cx * sin_theta + (d * kx) * (1 - cos_theta);
    *y = vy * cos_theta + cy * sin_theta + (d * ky) * (1 - cos_theta);
    *z = vz * cos_theta + cz * sin_theta + (d * kz) * (1 - cos_theta);
}

__host__ __device__
inline void velocity_cartesian2spherical(double x, double y, double z,
                                         double xdot, double ydot, double zdot,
                                         double* vR, double* vtheta, double* vphi)
{
    *vR = (x * xdot + y * ydot + z * zdot) / (sqrt(x * x + y * y + z * z));
    *vtheta = ((x * xdot + y * ydot) * z - (x * x + y * y) * zdot) / 
        ((x * x + y * y + z * z) * sqrt(x * x + y * y));
    *vphi = (x * ydot - xdot * y) / (x * x + y * y);
}

__host__ __device__
inline void spherical2cartesian(double R, double theta, double phi,
                                double* x, double* y, double* z)
{
    /*
    *x = sin(theta) * cos(phi) * R + cos(theta) * cos(phi) * theta - sin(phi) * phi;
    *y = sin(theta) * sin(phi) * R + cos(theta) * sin(phi) * theta + cos(phi) * phi;
    *z = cos(theta) * R - sin(theta) * theta;
    */
    *x = sin(theta) * cos(phi) * R;
    *y = sin(theta) * sin(phi) * R;
    *z = cos(theta) * R;
}

__host__ __device__
inline void cartesian2spherical(double x, double y, double z,
                                double* R_, double* theta_, double* phi_)
{
    /*
    double rho = sqrt(x*x + y*y + z*z);
    double theta = acos(z / rho);
    double phi = atan(y / x);
    *R_ = sin(theta) * cos(phi) * x + sin(theta) * sin(phi) * y + cos(theta) * z;
    *theta_ = cos(theta) * cos(phi) * x + cos(theta) * sin(phi) * y - sin(theta) * z;
    *phi_ = -sin(phi) * x + cos(phi) * y;
    */
    *R_ = sqrt(x*x + y*y + z*z);
    *theta_ = acos(z / *R_);
    *phi_ = atan(y / x);
}

__host__ __device__
inline double distance(double R0, double theta0, double phi0,
                       double R1, double theta1, double phi1)
{
    return sqrt(R0 * R0 + R1 * R1 - 2 * R0 * R1 *
                (sin(theta0) * sin(theta1) * cos(phi0 - phi1) + 
                 cos(theta0) * cos(theta1)));
}

__host__ __device__
inline double lerp(double v0, double v1, double t)
{
    return (1 - t) * v0 + t * v1;
    //return v0 + t * (v1 - v0);
}
