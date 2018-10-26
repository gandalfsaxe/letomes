"""
Equations of motion for R4B-3D system (Restricted 4-Body Problem in 3 Dimensions).
Derived via Hamiltons's equations.

1. `analyticals.py`: set up the equations of motion.

2. `integrators.py`: discretize the equations of motion and defines a single time step of the
    chosen numerical algorithm.

3. `simulators.py`: run the single steps from `integrators.py` repeatedly for some initial
    conditions and stopping conditions.
"""
from math import cos, sin, sqrt, tan, acos, atan, pi

from numba import njit

from orbsim.r4b_3d import ETA_EARTH, ETA_MARS, ETA_SUN

eta_ks = [ETA_SUN, ETA_EARTH, ETA_MARS]


# @njit
def get_Rdot(B_r):
    """Rdot(R, theta, phi, B_r, B_theta, B_phi) from Hamilton's equations"""
    return B_r


# @njit
def get_thetadot(R, B_theta):
    """thetadot(R, theta, phi, B_r, B_theta, B_phi) from Hamilton's equations"""
    return B_theta / (R ** 2)


# @njit
def get_phidot(R, theta, B_phi):
    """phidot(R, theta, phi, B_r, B_theta, B_phi) from Hamilton's equations"""
    return B_phi / (R ** 2 * sin(theta) ** 2)


# @njit
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


# @njit
def Bdot_denominator(R, theta, phi, R_k, theta_k, phi_k):
    """fraction denominator for generalized momenta Bdot"""
    base = (R - R_k) ** 2 * (
        cos(theta) * cos(theta_k) + sin(theta) * sin(theta_k) * cos(phi - phi_k)
    )
    print("base: {}".format(base))
    return base * sqrt(base)


# @njit
def Bdot_numerators(R, theta, phi, R_k, theta_k, phi_k):
    """fraction numerators for generalized momenta Bdot"""
    n1 = -(
        R
        - R_k
        * (cos(theta) * cos(theta_k) + (sin(theta) * sin(theta_k * cos(phi - phi_k))))
    )
    n2 = (
        R
        * R_k
        * (-sin(theta) * cos(theta_k) + cos(theta) * sin(theta_k) * cos(phi - phi_k))
    )
    n3 = -R * R_k * sin(theta) * sin(theta_k) * sin(phi - phi_k)
    return (n1, n2, n3)


# TODO: Region


def get_xyz(r, theta, phi):  # TODO: Optimize speed later
    x = r * sin(theta) * cos(phi)
    y = r * sin(theta) * sin(phi)
    z = r * cos(theta)

    return x, y, z


def get_spherical(x, y, z):  # TODO: Optimize speed later
    r = sqrt(x ** 2 + y ** 2 + z ** 2)
    theta = acos(z / r)
    if x >= 0:
        phi = atan(y / x)
    elif y >= 0:
        phi = atan(y / x) + pi
    else:
        phi = atan(y / x) - pi

    return r, theta, phi


def get_distance_xyz(x1, y1, z1, x2, y2, z2):
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def get_distance_spherical(r1, theta1, phi1, r2, theta2, phi2):
    return sqrt(
        r1 ** 2
        + r2 ** 2
        - 2
        * r1
        * r2
        * (
            cos(theta1) * cos(theta2)
            + sin(theta1)
            * sin(theta2)
            * (cos(phi1) * cos(phi2) + sin(phi1) * sin(phi2))
        )
    )

