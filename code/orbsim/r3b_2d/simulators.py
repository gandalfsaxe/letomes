import time

import numpy as np
from numba import njit

from . import (
    UNIT_TIME,
    UNIT_VELOCITY,
    LEO_RADIUS_NONDIM,
    EARTH_POSITION_X,
    LEO_VELOCITY_NONDIM,
)
from .integrators import symplectic


@njit
def run_sim(psi, duration=3, max_iter=1e7):
    """
    return: [Dv, [x, y, px, py, h]]
    launch (not really a launch since we start from LEO) a 
    single rocket with a given set of hyperparameters, return the resulting path
    """
    pos_ang, burn_ang, burnDv = psi  # extract parameters from decision vector
    burnDv /= UNIT_VELOCITY
    duration /= UNIT_TIME

    """define init params"""
    # position (where on earth do we start our burn)
    x0 = np.cos(pos_ang) * LEO_RADIUS_NONDIM
    y0 = np.sin(pos_ang) * LEO_RADIUS_NONDIM
    x0 += EARTH_POSITION_X

    # how fast are we going when we start?
    vhat_x = -np.sin(pos_ang)
    vhat_y = np.cos(pos_ang)
    v_x = (LEO_VELOCITY_NONDIM) * vhat_x
    v_y = (LEO_VELOCITY_NONDIM) * vhat_y

    # burn vector: At what angle do we launch outward, and how hard do we push?
    burnDv_x = np.cos(burn_ang) * vhat_x - np.sin(burn_ang) * vhat_y
    burnDv_y = np.sin(burn_ang) * vhat_x + np.cos(burn_ang) * vhat_y

    # resultant momentum vector
    p0_x = v_x + burnDv * burnDv_x - y0
    p0_y = v_y + burnDv * burnDv_y + x0

    """SIMULATE"""
    # print(f"running symplectic with [x0, y0, p0_x, p0_y]{[x0, y0, p0_x, p0_y]}")
    # starttime = time.time()
    score = [0.0]
    success = [0]
    path = symplectic(
        x0, y0, p0_x, p0_y, score, success, duration=duration, max_iter=int(max_iter)
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

