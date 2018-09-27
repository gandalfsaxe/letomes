"""
Implements symplectic integrators that integrates H-R4B system equations.
"""

# import time
from math import pi, sin

from numba import njit  # boolean, float64, jit

from orbsim.r4b_3d import (
    LEO_RADIUS_NONDIM,
    LEO_VELOCITY_NONDIM,
    UNIT_LENGTH,
    UNIT_TIME,
    UNIT_VELOCITY,
    h_DEFAULT,
    h_MIN_DEFAULT,
)
from orbsim.r4b_3d.analyticals import get_Bdot


# @njit
def euler_step_symplectic(ephemerides_on_date, h, R, theta, phi, B_r, B_theta, B_phi):
    """Takes a single time step of the symplectic Euler algorithm"""
    # Update q
    R = R + h * B_r
    theta = theta + h * B_theta / R ** 2
    phi = phi + h * B_phi / (R ** 2 + sin(theta) ** 2)

    # Get ephemeris and Bdots
    R_ks = []
    theta_ks = []
    phi_ks = []

    for _, eph in ephemerides_on_date.items():
        R_ks.append(eph["r"])
        theta_ks.append(eph["theta"] * pi / 180)
        phi_ks.append(eph["phi"] * pi / 180)

    Bdot_r, Bdot_theta, Bdot_phi = get_Bdot(
        R, theta, phi, B_theta, B_phi, R_ks, theta_ks, phi_ks
    )

    # Update p
    B_r = B_r + h * Bdot_r
    B_theta = B_theta + h * Bdot_theta
    B_phi = B_phi + h * Bdot_phi

    return R, theta, phi, B_r, B_theta, B_phi


# @njit
# def verlet_step_symplectic(h, x, y, p_x, p_y):
#     """Takes a half step, then another half step in the symplectic Verlet algorithm"""
#     hh = 0.5 * h
#     denominator = 1.0 / (1.0 + hh ** 2)
#     # Step 1
#     v_x = get_v_x(y, p_x)
#     x = (x + (v_x + p_y * hh) * hh) * denominator
#     # Step 2
#     v_y = get_v_y(x, p_y)
#     y = y + v_y * hh
#     # Step 2
#     pdot_x = get_pdot_x(x, y, p_y)
#     pdot_y = get_pdot_y(x, y, p_x)
#     p_x = (p_x + (2.0 * pdot_x + (2 * pdot_y + p_x) * hh) * hh) * denominator
#     p_y = (
#         p_y + (pdot_y + get_pdot_y(x, y, p_x)) * hh
#     )  # TODO: mixed, what's correct? Derive theory
#     # Step 3
#     v_x = get_v_x(y, p_x)
#     v_y = get_v_y(x, p_y)
#     x += v_x * hh
#     y += v_y * hh

#     return x, y, p_x, p_y


# @njit
# def relative_error(vec1, vec2):
#     x1, y1 = vec1
#     x2, y2 = vec2
#     return sqrt(((x2 - x1) ** 2 + (y2 - y1) ** 2) / (x2 ** 2 + y2 ** 2))
