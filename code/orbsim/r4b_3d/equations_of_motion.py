"""
Equations of motion for R4B-3D system (Restricted 4-Body Problem in 3 Dimensions),
derived via Hamiltons's equations.

Includes at least:
- 3 Qdot: coordinate differential equations in spherical coordinates.
- 3 Pdot: generalized momentum differential equations in spherical coordinates.
- 3 P: generalized momentum as function of Qdot.
- Hamiltonian

All non-dimensionalized and scaled with mass of spacecraft (see derivations in report)
"""

from math import pi

import numpy as np
from numpy import cos, sin, sqrt, tan

from orbsim.r4b_3d import EARTH_ETA, MARS_ETA, SUN_ETA

eta_ks = [SUN_ETA, EARTH_ETA, MARS_ETA]


# region Coodinate Derivatives: Qdot(Q, B)
def get_Rdot(B_R):
    """Rdot(R, theta, phi, B_R, B_theta, B_phi) from Hamilton's equations"""
    return B_R


def get_thetadot(R, B_theta):
    """thetadot(R, theta, phi, B_R, B_theta, B_phi) from Hamilton's equations"""
    if R <= 0:
        raise ValueError("R must be positive.")
    return B_theta / (R ** 2)


def get_phidot(R, theta, B_phi):
    """phidot(R, theta, phi, B_R, B_theta, B_phi) from Hamilton's equations"""

    if R <= 0:
        raise ValueError("R cannot be less than or equal to zero.")
    elif theta <= 0 or theta >= pi:
        raise ValueError("theta must be in range 0 < theta < pi.")

    return B_phi / (R ** 2 * sin(theta) ** 2)


# endregion

# region Momentum Derivatives: Bdot(Q, B, Qk)
def get_Bdot_R(R, theta, phi, B_theta, B_phi, R_ks, theta_ks, phi_ks):
    """
    Gives Bdot_R, i.e. the time derivative of the generalized momentum in R direction,
    per unit mass and in chosen characteristic units.

    Arguments:
        R {float} -- R coordinate (AU)
        theta {float} -- theta coordinate (rad)
        phi {float} -- phi coordinate (rad)
        B_theta {float} -- B_theta momentum (linear velocity in R direction, AU/y)
        B_phi {float} -- B_theta (angular theta momentum per mass, AU^2/y)
        R_ks {List(float)} -- Coordinates [R_sun, R_earth, R_mars], AU
        theta_ks {List(float)} -- Coordinates [theta_sun, theta_earth, theta_mars], rad
        phi_ks {List(float)} -- Coordinates [phi_sun, phi_earth, phi_mars], rad

    Raises:
        ValueError -- Out of range coordinates.

    Returns:
        float -- Bdot_R
    """

    if R <= 0:
        raise ValueError("R cannot be less than or equal to zero.")
    if theta <= 0 or theta >= pi:
        raise ValueError("theta must be in range 0 < theta < pi.")
    if phi <= -pi or phi > pi:
        raise ValueError("phi must be in range -pi < phi <= pi.")

    for R_k in R_ks:
        if R_k < 0:
            raise ValueError("All R_k must zero or be positive (allow for SUN_R = 0)")
    for theta_k in theta_ks:
        if theta_k <= 0 or theta_k >= pi:
            raise ValueError("theta_k must be in range 0 < theta_k < pi.")
    for phi_k in phi_ks:
        if phi_k <= -pi or phi_k > pi:
            raise ValueError("phi_k must be in range -pi < phi_k <= pi.")

    R_ks = np.array(R_ks)
    theta_ks = np.array(theta_ks)
    phi_ks = np.array(phi_ks)

    numerators = eta_ks * (
        -R
        + R_ks
        * (cos(theta) * cos(theta_ks) + sin(theta) * sin(theta_ks) * cos(phi - phi_ks))
    )

    denominators_base = (
        R ** 2
        + R_ks ** 2
        - 2
        * R
        * R_ks
        * (cos(theta) * cos(theta_ks) + sin(theta) * sin(theta_ks) * cos(phi - phi_ks))
    )

    denominators = denominators_base * sqrt(denominators_base)

    summation = np.sum(numerators / denominators)

    Bdot_R1 = B_theta ** 2 / (R ** 3)
    Bdot_R2 = B_phi ** 2 / (R ** 3 * sin(theta) ** 2)
    Bdot_R3 = summation

    Bdot_R = Bdot_R1 + Bdot_R2 + Bdot_R3

    return Bdot_R


def get_Bdot_theta(R, theta, phi, B_phi, R_ks, theta_ks, phi_ks):
    """
    Gives Bdot_theta, i.e. the time derivative of the generalized momentum in theta
    direction, per unit mass and in chosen characteristic units.

    Arguments:
        R {float} -- R coordinate (AU)
        theta {float} -- theta coordinate (rad)
        phi {float} -- phi coordinate (rad)
        B_phi {float} -- B_theta (angular theta momentum per mass, AU^2/y)
        R_ks {List(float)} -- Coordinates [R_sun, R_earth, R_mars], AU
        theta_ks {List(float)} -- Coordinates [theta_sun, theta_earth, theta_mars], rad
        phi_ks {List(float)} -- Coordinates [phi_sun, phi_earth, phi_mars], rad

    Raises:
        ValueError -- Out of range coordinates.

    Returns:
        float -- Bdot_theta
    """

    if R <= 0:
        raise ValueError("R cannot be less than or equal to zero.")
    if theta <= 0 or theta >= pi:
        raise ValueError("theta must be in range 0 < theta < pi.")
    if phi <= -pi or phi > pi:
        raise ValueError("phi must be in range -pi < phi <= pi.")

    for R_k in R_ks:
        if R_k < 0:
            raise ValueError("All R_k must zero or be positive (allow for SUN_R = 0)")
    for theta_k in theta_ks:
        if theta_k <= 0 or theta_k >= pi:
            raise ValueError("theta_k must be in range 0 < theta_k < pi.")
    for phi_k in phi_ks:
        if phi_k <= -pi or phi_k > pi:
            raise ValueError("phi_k must be in range -pi < phi_k <= pi.")

    R_ks = np.array(R_ks)
    theta_ks = np.array(theta_ks)
    phi_ks = np.array(phi_ks)

    numerators = eta_ks * (
        R
        * R_ks
        * (-sin(theta) * cos(theta_ks) + cos(theta) * sin(theta_ks) * cos(phi - phi_ks))
    )

    denominators_base = (
        R ** 2
        + R_ks ** 2
        - 2
        * R
        * R_ks
        * (cos(theta) * cos(theta_ks) + sin(theta) * sin(theta_ks) * cos(phi - phi_ks))
    )

    denominators = denominators_base * sqrt(denominators_base)

    summation = np.sum(numerators / denominators)

    Bdot_theta1 = B_phi ** 2 / (R ** 2 * sin(theta) ** 2 * tan(theta))
    Bdot_theta2 = summation

    Bdot_theta = Bdot_theta1 + Bdot_theta2

    return Bdot_theta


def get_Bdot_phi(R, theta, phi, R_ks, theta_ks, phi_ks):
    """
    Gives Bdot_phi, i.e. the time derivative of the generalized momentum in theta
    direction, per unit mass and in chosen characteristic units.

    Arguments:
        R {float} -- R coordinate (AU)
        theta {float} -- theta coordinate (rad)
        phi {float} -- phi coordinate (rad)
        R_ks {List(float)} -- Coordinates [R_sun, R_earth, R_mars], AU
        theta_ks {List(float)} -- Coordinates [theta_sun, theta_earth, theta_mars], rad
        phi_ks {List(float)} -- Coordinates [phi_sun, phi_earth, phi_mars], rad

    Raises:
        ValueError -- Out of range coordinates.

    Returns:
        float -- Bdot_phi
    """

    if R <= 0:
        raise ValueError("R cannot be less than or equal to zero.")
    if theta <= 0 or theta >= pi:
        raise ValueError("theta must be in range 0 < theta < pi.")
    if phi <= -pi or phi > pi:
        raise ValueError("phi must be in range -pi < phi <= pi.")

    for R_k in R_ks:
        if R_k < 0:
            raise ValueError("All R_k must zero or be positive (allow for SUN_R = 0)")
    for theta_k in theta_ks:
        if theta_k <= 0 or theta_k >= pi:
            raise ValueError("theta_k must be in range 0 < theta_k < pi.")
    for phi_k in phi_ks:
        if phi_k <= -pi or phi_k > pi:
            raise ValueError("phi_k must be in range -pi < phi_k <= pi.")

    R_ks = np.array(R_ks)
    theta_ks = np.array(theta_ks)
    phi_ks = np.array(phi_ks)

    numerators = eta_ks * (-R * R_ks * sin(theta) * sin(theta_ks) * sin(phi - phi_ks))

    denominators_base = (
        R ** 2
        + R_ks ** 2
        - 2
        * R
        * R_ks
        * (cos(theta) * cos(theta_ks) + sin(theta) * sin(theta_ks) * cos(phi - phi_ks))
    )

    denominators = denominators_base * sqrt(denominators_base)

    summation = np.sum(numerators / denominators)

    Bdot_phi = summation

    return Bdot_phi


# endregion

# region Momenta B(Q, Qdot) - Derived from Qdot(Q, B)
def get_B_R(Rdot):
    """Get B_R from Q, Qdot"""

    return Rdot


def get_B_theta(R, thetadot):
    """Get B_theta from Q, Qdot"""
    if R <= 0:
        raise ValueError("R cannot be less than or equal to zero.")

    return R ** 2 * thetadot


def get_B_phi(R, theta, phidot):
    """Get B_phi from Q, Qdot"""
    if R <= 0:
        raise ValueError("R cannot be less than or equal to zero.")
    if theta <= 0 or theta >= pi:
        raise ValueError("theta must be in range 0 < theta < pi.")

    return R ** 2 * sin(theta) ** 2 * phidot


# endregion


# if __name__ == "__main__":

#     from pprint import pprint

#     pprint(
#         get_Bdot_R(
#             1.1,
#             3.1315926535897933,
#             3.141592653589793,
#             0.2,
#             -0.1,
#             [0.0, 0.983580560001, 1.470582878522],
#             [0.013707783890401887, 1.1997429598510756, 1.264411333882953],
#             [0.0, 2.0274978713480216, 6.283185307179586],
#         )
#     )
