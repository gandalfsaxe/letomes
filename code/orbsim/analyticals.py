from .constants import k
from numba import jit

"""
static functions that evaluate some expression formulated in the paper
"""

@jit
def get_Pdot_x(x, y, p_x, p_y):
    """from position and momentum vectors, returns generalized momentum, nondimensionalized"""
    denominator_1, denominator_2 = Pdot_denominator(x, y, p_x, p_y)
    return p_y - ((1 - k) * (x + k)) / denominator_1 + (k * (1 + k - x)) / denominator_2

@jit
def get_Pdot_y(x, y, p_x, p_y):
    denominator_1, denominator_2 = Pdot_denominator(x, y, p_x, p_y)
    return -p_x - ((1 - k) * y) / denominator_1 - (k * y) / denominator_2

@jit
def Pdot_denominator(x, y, p_x, p_y):
    denominator_1 = ((x + k) ** 2 + y ** 2) ** (3 / 2)
    denominator_2 = ((1 + k - x) ** 2 + y ** 2) ** (3 / 2)
    return denominator_1, denominator_2

