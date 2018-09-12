"""
Equations of motion for R3B-2D system (Restricted 3-Body Problem in 2 Dimensions).
Derived via Hamiltons's equations.
"""

from math import sqrt

from numba import njit

from . import k


@njit
def get_pdot_x(x, y, p_y):
    """generalized momentum p_x (nondimensionalized) from position and momentum vectors"""
    denominator_1, denominator_2 = pdot_denominators(x, y)
    pdot_x = (
        p_y - ((1 - k) * (x + k)) / denominator_1 - k * (x - 1 + k) / denominator_2
    )  # Note: In old version there was a sign error and "1+k-x" used to be "1-k-x"
    return pdot_x


@njit
def get_pdot_y(x, y, p_x):
    """generalized momentum p_y (nondimensionalized) from position and momentum vectors"""
    denominator_1, denominator_2 = pdot_denominators(x, y)
    pdot_y = -p_x - (1 - k) * y / denominator_1 - k * y / denominator_2
    return pdot_y


@njit
def pdot_denominators(x, y):
    """denominators used in get_pdot_x and get_pdot_y"""
    denominator_1 = ((x + k) ** 2 + y ** 2) * sqrt((x + k) ** 2 + y ** 2)
    denominator_2 = ((x - 1 + k) ** 2 + y ** 2) * sqrt(
        (x - 1 + k) ** 2 + y ** 2
    )  # Note: In old version there was a sign error and "1+k-x" used to be "1-k-x"
    return denominator_1, denominator_2


@njit
def get_xdot(y, p_x):
    """speed in x direction, from coordinates and momenta"""
    v_x = p_x + y
    return v_x


@njit
def get_ydot(x, p_y):
    """speed in y direction, from coordinates and momenta"""
    v_y = p_y - x
    return v_y
