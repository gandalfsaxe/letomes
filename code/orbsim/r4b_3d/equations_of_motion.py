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

from math import cos, sin, sqrt, tan

from orbsim.r4b_3d import ETA_EARTH, ETA_MARS, ETA_SUN

eta_ks = [ETA_SUN, ETA_EARTH, ETA_MARS]


# region Coodinate Derivatives: Qdot(Q, B)
def get_Rdot(B_r):
    """Rdot(R, theta, phi, B_r, B_theta, B_phi) from Hamilton's equations"""
    return B_r


def get_thetadot(R, B_theta):
    """thetadot(R, theta, phi, B_r, B_theta, B_phi) from Hamilton's equations"""
    return B_theta / (R ** 2)


def get_phidot(R, theta, B_phi):
    """phidot(R, theta, phi, B_r, B_theta, B_phi) from Hamilton's equations"""
    return B_phi / (R ** 2 * sin(theta) ** 2)


# endregion


# region Momentum Derivatives: Bdot(Q, B, eph)
def get_Bdot(R, theta, phi, B_theta, B_phi, R_ks, theta_ks, phi_ks):
    """
    All three Bdot from Hamilton's equations (Bdot_r, Bdot_theta and Bdot_phi)
    """
    # Initialize Bdot parts
    Bdot_r1 = B_theta ** 2 / (R ** 3)
    Bdot_r2 = B_phi ** 2 / (R ** 3 * sin(theta) ** 2)
    Bdot_r3 = 0
    Bdot_theta1 = B_phi ** 2 / (R ** 2 * sin(theta) ** 2 * tan(theta))
    Bdot_theta2 = 0
    Bdot_phi1 = 0
    # Everything under the summation
    for i, _ in enumerate(R_ks):
        numerator_1, numerator_2, numerator_3 = Bdot_numerators(
            R, theta, phi, R_ks[i], theta_ks[i], phi_ks[i]
        )
        denominator = Bdot_denominator(R, theta, phi, R_ks[i], theta_ks[i], phi_ks[i])
        Bdot_r3 += eta_ks[i] * numerator_1 / denominator
        Bdot_theta2 += eta_ks[i] * numerator_2 / denominator
        Bdot_phi1 += eta_ks[i] * numerator_3 / denominator
    # Add Bdot parts
    Bdot_r = Bdot_r1 + Bdot_r2 + Bdot_r3
    Bdot_theta = Bdot_theta1 + Bdot_theta2
    Bdot_phi = Bdot_phi1
    return Bdot_r, Bdot_theta, Bdot_phi


def Bdot_denominator(R, theta, phi, R_k, theta_k, phi_k):
    """fraction denominator for generalized momenta Bdot"""
    base = (
        R ** 2
        + R_k ** 2
        - 2
        * R
        * R_k
        * (cos(theta) * cos(theta_k) + sin(theta) * sin(theta_k) * cos(phi - phi_k))
    )

    return base * sqrt(base)


def Bdot_numerators(R, theta, phi, R_k, theta_k, phi_k):
    """fraction numerators for generalized momenta Bdot"""
    n1 = -R + R_k * (
        cos(theta) * cos(theta_k) + (sin(theta) * sin(theta_k * cos(phi - phi_k)))
    )
    n2 = (
        R
        * R_k
        * (-sin(theta) * cos(theta_k) + cos(theta) * sin(theta_k) * cos(phi - phi_k))
    )
    n3 = -R * R_k * sin(theta) * sin(theta_k) * sin(phi - phi_k)
    return (n1, n2, n3)


# endregion


# region Momenta B(Q, Qdot) - Derived from Qdot(Q, B)
def get_B_r(Rdot):
    """Get B_r from Q, Qdot"""

    return Rdot


def get_B_theta(R, thetadot):
    """Get B_theta from Q, Qdot"""
    return R ** 2 * thetadot


def get_B_phi(R, theta, phidot):
    """Get B_phi from Q, Qdot"""
    return R ** 2 * sin(theta) ** 2 * phidot


# endregion
