"""
Equations of motion for R3B-2D system (Restricted 3-Body Problem in 2 Dimensions).
Derived via Hamiltons's equations.
"""

from math import cos, sin, sqrt, tan

from numba import njit


@njit
def get_Rdot(B_r):
    return B_r


@njit
def get_thetadot(B_theta, R):
    return B_theta / (R ** 2)


@njit
def get_phidot(B_phi, R, theta):
    return B_phi / (R ** 2 * sin(theta) ** 2)


@njit
def Bdot(B_theta, B_phi, R, theta, phi, nus, Rs, thetas, phis):
    r_p1 = B_theta ** 2 / (R ** 3)
    r_p2 = B_phi ** 2 / (R ** 3)
    r_p3 = 0
    theta_p1 = B_phi ** 2 / (R ** 2 * sin(theta) ** 2 * tan(theta))
    theta_p2 = 0
    phi_p1 = 0
    for i in range(len(Rs)):
        numerator_1, numerator_2, numerator_3 = Bdot_numerators(
            R, Rs[i], theta, thetas[i], phi, phis[i]
        )
        denominator = Bdot_denominators(R, Rs[i], theta, thetas[i], phi, phis[i])
        r_p3 += nus[i] * numerator_1 / denominator
        theta_p2 += nus[i] * numerator_2 / denominator
        phi_p1 += nus[i] * numerator_3 / denominator
    Bdot_r = r_p1 + r_p2 + r_p3
    Bdot_theta = theta_p1 + theta_p2
    Bdot_phi = phi_p1
    return Bdot_r, Bdot_theta, Bdot_phi


@njit
def Bdot_denominators(R, R_i, theta, theta_i, phi, phi_i):
    base = (R - R_i) ** 2 * (
        cos(theta) * cos(theta_i) + sin(theta) * sin(theta_i) * cos(phi - phi_i)
    )
    return base * sqrt(base)


@njit
def Bdot_numerators(R, R_i, theta, theta_i, phi, phi_i):
    n1 = -(
        R
        - R_i
        * (cos(theta) * cos(theta_i) + (sin(theta) * sin(theta_i * cos(phi - phi_i))))
    )
    n2 = (
        R
        * R_i
        * (-sin(theta) * cos(theta_i) + cos(theta) * sin(theta_i) * cos(phi - phi_i))
    )
    n3 = -R * R_i * sin(theta) * sin(theta_i) * sin(phi - phi_i)
    return (n1, n2, n3)
