"""
Equations of motion for R3B-2D system (Restricted 3-Body Problem in 2 Dimensions).
Derived via Hamiltons's equations.
"""

from math import sqrt

from numba import njit

from . import k


@njit
def get_pdot_x(x, y, p_y):
    """from position and momentum vectors, returns generalized momentum, nondimensionalized"""
    denominator_1, denominator_2 = pdot_denominators(x, y, k)
    pdot_x = (
        p_y - ((1 - k) * (x + k)) / denominator_1 + k * (1 + k - x) / denominator_2
    )  # FIXME: Should be "1 + k - x"
    return pdot_x


@njit
def get_pdot_y(x, y, p_x):
    denominator_1, denominator_2 = pdot_denominators(x, y, k)
    pdot_y = -p_x - (1 - k) * y / denominator_1 - k * y / denominator_2
    return pdot_y


@njit
def pdot_denominators(x, y, k):
    denominator_1 = ((x + k) ** 2 + y ** 2) * sqrt((x + k) ** 2 + y ** 2)
    denominator_2 = ((1 + k - x) ** 2 + y ** 2) * sqrt(
        (1 + k - x) ** 2 + y ** 2
    )  # FIXME: Should be "1 + k - x"
    return denominator_1, denominator_2


@njit
def get_v_x(y, p_x):
    v_x = p_x + y
    return v_x


@njit
def get_v_y(x, p_y):
    v_y = p_y - x
    return v_y
