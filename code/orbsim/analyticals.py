from .constants import k


"""
static functions that evaluate some expression formulated in the paper
"""


def Pdot(x, y, p_x, p_y):
    """from position and momentum vectors, returns generalized momentum, nondimensionalized"""
    Pdot_x = (
        p_y
        - ((1 - k) * (x + k)) / ((x + k) ** 2 + y ** 2) ** (3 / 2)
        + (k * (1 + k - x)) / ((1 + k - x) ** 2 + y ** 2) ** (3 / 2)
    )
    Pdot_y = (
        -p_x
        - ((1 - k) * y) / ((x + k) ** 2 + y ** 2) ** (3 / 2)
        - (k * y) / ((1 + k - x) ** 2 + y ** 2) ** (3 / 2)
    )
    return [Pdot_x, Pdot_y]
