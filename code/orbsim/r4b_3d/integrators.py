"""
Implements symplectic integrators that integrates H-R4B system equations.

1. `analyticals.py`: set up the equations of motion.

2. `integrators.py`: discretize the equations of motion and defines a single time step of the
    chosen numerical algorithm.

3. `simulation.py`: run the single steps from `integrators.py` repeatedly for some initial
    conditions and stopping conditions.
"""
from math import pi

import numpy as np
from numpy import cos, sin, sqrt, tan

from orbsim.r4b_3d import EARTH_ETA, MARS_ETA, SUN_ETA
from orbsim.r4b_3d.coordinate_system import (
    keep_phi_in_interval_npi_to_pi,
    keep_theta_in_interval_zero_to_pi,
)
from orbsim.r4b_3d.equations_of_motion import (
    get_Bdot_phi,
    get_Bdot_R,
    get_Bdot_theta,
    get_phidot,
    get_Rdot,
    get_thetadot,
)

eta_ks = [SUN_ETA, EARTH_ETA, MARS_ETA]

# from numba import njit  # boolean, float64, jit


# @njit
def euler_step_symplectic(h, Q, B, eph_coords):
    """Takes a single time step of the symplectic Euler algorithm"""
    # Unpack Q, B and eph_coords
    R, theta, phi = Q
    B_R, B_theta, B_phi = B
    R_ks, theta_ks, phi_ks = eph_coords

    # Update q
    R = R + h * get_Rdot(B_R)
    theta = theta + h * get_thetadot(R, B_theta)
    phi = phi + h * get_phidot(R, theta, B_phi)

    if theta <= 0 or theta >= pi:
        theta = keep_theta_in_interval_zero_to_pi(theta)
    if phi <= -pi or phi > pi:
        phi = keep_phi_in_interval_npi_to_pi(phi)

    # Update B_R
    Bdot_R = get_Bdot_R(R, theta, phi, B_theta, B_phi, R_ks, theta_ks, phi_ks)
    B_R = B_R + h * Bdot_R

    # Update B_theta
    Bdot_theta = get_Bdot_theta(R, theta, phi, B_phi, R_ks, theta_ks, phi_ks)
    B_theta = B_theta + h * Bdot_theta

    # Update B_phi
    Bdot_phi = get_Bdot_phi(R, theta, phi, R_ks, theta_ks, phi_ks)
    B_phi = B_phi + h * Bdot_phi

    return ((R, theta, phi), (B_R, B_theta, B_phi))


# @njit
def verlet_step_symplectic(h, Q, B, eph_coords):
    """Takes a single time step of the symplectic Euler algorithm"""
    # Unpack Q, B and eph_coords
    R0, theta0, phi0 = Q
    B_R0, B_theta0, B_phi0 = B
    R_ks, theta_ks, phi_ks = eph_coords

    hh = h / 2

    # Update Qh
    R_h = R0 + hh * B_R0
    theta_h = theta0 + hh * B_theta0 / R_h ** 2
    phi_h = phi0 + hh * B_phi0 / (R_h ** 2 * sin(theta_h) ** 2)

    Q_h = [R_h, theta_h, phi_h]

    # Update B1
    lambda_hks = get_lambda_hks(Q_h, eph_coords)

    gamma_hks = get_gamma_hks(Q_h, eph_coords)
    summation_gamma = np.sum(gamma_hks / lambda_hks)
    B_phi1 = B_phi0 + hh * (2 * summation_gamma)

    beta_hks = get_beta_hks(Q_h, eph_coords)
    summation_beta = np.sum(beta_hks / lambda_hks)
    B_theta1 = B_theta0 + hh * (
        (B_phi0 ** 2 + B_phi1 ** 2) / (R_h ** 2 * sin(theta_h) ** 2 * tan(theta_h))
        + 2 * summation_beta
    )

    alpha_hks = get_alpha_hks(Q_h, eph_coords)
    summation_alpha = np.sum(beta_hks / lambda_hks)
    B_R1 = B_R0 + hh * (
        (B_theta0 ** 2 + B_theta1 ** 2) / (R_h ** 3)
        + (B_phi0 ** 2 + B_phi1 ** 2) / (R_h ** 3 * sin(theta_h) ** 2)
        + 2 * summation_alpha
    )

    # Update Q1
    R1 = R_h + hh * B_R1
    theta1 = theta_h + hh * (B_theta1 / R_h ** 2)
    phi1 = phi_h + hh * (B_phi1 / (R_h ** 2 * sin(theta_h) ** 2))

    Q1 = [R1, theta1, phi1]
    B1 = [B_R1, B_theta1, B_phi1]

    return Q1, B1


def get_lambda_hks(Q_h, eph_coords):
    # Unpack Q_h, B and eph_coords
    R_h, theta_h, phi_h = Q_h
    R_ks, theta_ks, phi_ks = eph_coords

    R_ks = np.array(R_ks)
    theta_ks = np.array(theta_ks)
    phi_ks = np.array(phi_ks)

    denominators_base = (
        R_h ** 2
        + R_ks ** 2
        - 2
        * R_h
        * R_ks
        * (
            cos(theta_h) * cos(theta_ks)
            + sin(theta_h) * sin(theta_ks) * cos(phi_h - phi_ks)
        )
    )

    denominators = denominators_base * sqrt(denominators_base)

    return denominators


def get_gamma_hks(Q_h, eph_coords):
    # Unpack Q_h, B and eph_coords
    R_h, theta_h, phi_h = Q_h
    R_ks, theta_ks, phi_ks = eph_coords

    R_ks = np.array(R_ks)
    theta_ks = np.array(theta_ks)
    phi_ks = np.array(phi_ks)

    numerators = eta_ks * (
        -R_h * R_ks * sin(theta_h) * sin(theta_ks) * sin(phi_h - phi_ks)
    )

    return numerators


def get_beta_hks(Q_h, eph_coords):
    # Unpack Q_h, B and eph_coords
    R_h, theta_h, phi_h = Q_h
    R_ks, theta_ks, phi_ks = eph_coords

    R_ks = np.array(R_ks)
    theta_ks = np.array(theta_ks)
    phi_ks = np.array(phi_ks)

    numerators = eta_ks * (
        R_h
        * R_ks
        * (
            -sin(theta_h) * cos(theta_ks)
            + cos(theta_h) * sin(theta_ks) * cos(phi_h - phi_ks)
        )
    )

    return numerators


def get_alpha_hks(Q_h, eph_coords):
    # Unpack Q_h, B and eph_coords
    R_h, theta_h, phi_h = Q_h
    R_ks, theta_ks, phi_ks = eph_coords

    R_ks = np.array(R_ks)
    theta_ks = np.array(theta_ks)
    phi_ks = np.array(phi_ks)

    numerators = eta_ks * (
        -R_h
        + R_ks
        * (
            cos(theta_h) * cos(theta_ks)
            + sin(theta_h) * sin(theta_ks) * cos(phi_h - phi_ks)
        )
    )

    return numerators


# @njit
# def relative_error(vec1, vec2):
#     x1, y1 = vec1
#     x2, y2 = vec2
#     return sqrt(((x2 - x1) ** 2 + (y2 - y1) ** 2) / (x2 ** 2 + y2 ** 2))

# if __name__ == "__main__":

#     from pprint import pprint

#     test = euler_step_symplectic(
#         3.1687536450894706e-08,
#         [0.9833550575288669, 1.1683216354741335, 1.7605747565734895],
#         [0.06619397691044351, 0.6131467542061076, 8.857580619176503],
#         [
#             [0.0, 0.983311354517, 1.45349465364],
#             [0.7853981633974483, 1.1683216629370692, 1.3089386258001088],
#             [0.0, 1.7605751533054472, 0.681572830178241],
#         ],
#     )

#     pass
