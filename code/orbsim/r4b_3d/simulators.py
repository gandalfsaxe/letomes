# import time

from math import cos, sin, sqrt, acos, atan, pi

import numpy as np
from numba import njit

from orbsim.r4b_3d import (
    LEO_RADIUS_NONDIM,
    LEO_VELOCITY_NONDIM,
    UNIT_TIME,
    UNIT_VELOCITY,
)
from orbsim.r4b_3d.analyticals import get_xyz, get_spherical
from orbsim.r4b_3d.ephemerides import get_ephemerides
from orbsim.r4b_3d.integrators import simulate


# @njit
def launch_sim(psi, duration=3, max_iter=1e7):
    """
    return: [Dv, [x, y, px, py, h]]
    launch (not really a launch since we start from LEO) a
    single rocket with a given set of hyperparameters, return the resulting path
    """
    t_day, burnDv = psi  # extract parameters from decision vector
    burnDv /= UNIT_VELOCITY
    duration /= UNIT_TIME

    # Read ephemerides
    ephemerides = get_ephemerides()

    day_zero_eph = ephemerides["earth"].iloc[0]

    earth_r0 = day_zero_eph["r"]
    earth_theta0 = day_zero_eph["theta"] * pi / 180
    earth_phi0 = day_zero_eph["phi"] * pi / 180
    # earth_x0 = day_zero_eph["x"]
    # earth_y0 = day_zero_eph["y"]
    # earth_z0 = day_zero_eph["z"]

    # Get initial position of earth
    earth_position_x, earth_position_y, earth_position_z = get_xyz(
        earth_r0, earth_theta0, earth_phi0
    )

    """define init params"""
    # position (where on earth do we start our burn)
    x0 = LEO_RADIUS_NONDIM  # geocentric
    y0 = 0  # geocentric
    z0 = 0  # geocentric
    x0 += earth_position_x  # heliocentric
    y0 += earth_position_y  # heliocentric
    z0 += earth_position_z  # heliocentric

    # how fast are we going when we start?
    earth_velocity_x = -6.282939073970666
    earth_velocity_y = -1.0714089257187907
    earth_velocity_z = -0.4643489045706851

    v_x0 = LEO_VELOCITY_NONDIM + earth_velocity_x
    v_y0 = earth_velocity_y
    v_z0 = earth_velocity_z

    # burn vector: At what angle do we launch outward, and how hard do we push?'
    # We choose fixed burn angle = 0, kept for R3B comparison purposes
    burnDv_x = 1
    burnDv_y = 0
    burnDv_z = 0

    # R, theta, phi and their velocities
    R0, theta0, phi0 = get_spherical(x0, y0, z0)
    R0dot, theta0dot, phi0dot = get_spherical(v_x0, v_y0, v_z0)

    # resultant momentum vector
    B_r0 = R0dot
    B_theta0 = R0 ** 2 * theta0dot
    B_phi0 = R0 ** 2 * sin(theta0) ** 2 * phi0dot

    """SIMULATE"""
    # print(f"running symplectic with [x0, y0, p0_x, p0_y]{[x0, y0, p0_x, p0_y]}")
    # starttime = time.time()
    score = [0.0]
    success = [0]
    path = simulate(
        R0,
        theta0,
        phi0,
        B_r0,
        B_theta0,
        B_phi0,
        score,
        success,
        duration=duration,
        max_iter=int(max_iter),
    )

    # return success[0], score[0], path
    if success[0] == 1:
        # print("SUCCESS")
        final_score = score[0] + burnDv
        # print("score = ", final_score)
    else:
        final_score = (1 + score[0]) * 10
        # print("score = ", final_score)

    return final_score, path


if __name__ == "__main__":
    launch_sim([0, 0])

