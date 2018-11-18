"""
Implements symplectic integrators that integrates H-R4B system equations.

1. `analyticals.py`: set up the equations of motion.

2. `integrators.py`: discretize the equations of motion and defines a single time step of the
    chosen numerical algorithm.

3. `simulators.py`: run the single steps from `integrators.py` repeatedly for some initial
    conditions and stopping conditions.
"""

#  import logging

# import time

from orbsim.r4b_3d.equations_of_motion import (
    get_Rdot,
    get_thetadot,
    get_phidot,
    get_Bdot_R,
    get_Bdot_theta,
    get_Bdot_phi,
)

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
