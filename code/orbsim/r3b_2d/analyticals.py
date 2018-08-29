from math import sqrt, cos, sin, tan

from numba import njit

from . import k


"""
static functions that evaluate some expression formulated in the paper
"""


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


@njit
def get_Rdot(B_r):
    return B_r


@njit
def get_thetadot(B_theta, R):
    return B_theta / (R ** 2)


@njit
def get_phidot(B_phi, R, theta):
    return B_phi / (R ** 2 * sin(theta) ** 2)


@njit
def Bdot(B_theta, B_phi, R, theta, phi, nus, Rs, thetas, phis):
    r_p1 = B_theta ** 2 / (R ** 3)
    r_p2 = B_phi ** 2 / (R ** 3)
    r_p3 = 0
    theta_p1 = B_phi ** 2 / (R ** 2 * sin(theta) ** 2 * tan(theta))
    theta_p2 = 0
    phi_p1 = 0
    for i in range(len(Rs)):
        numerator_1, numerator_2, numerator_3 = Bdot_numerators(
            R, Rs[i], theta, thetas[i], phi, phis[i]
        )
        denominator = Bdot_denominators(R, Rs[i], theta, thetas[i], phi, phis[i])
        r_p3 += nus[i] * numerator_1 / denominator
        theta_p2 += nus[i] * numerator_2 / denominator
        phi_p1 += nus[i] * numerator_3 / denominator
    Bdot_r = r_p1 + r_p2 + r_p3
    Bdot_theta = theta_p1 + theta_p2
    Bdot_phi = phi_p1
    return Bdot_r, Bdot_theta, Bdot_phi


@njit
def Bdot_denominators(R, R_i, theta, theta_i, phi, phi_i):
    base = (R - R_i) ** 2 * (
        cos(theta) * cos(theta_i) + sin(theta) * sin(theta_i) * cos(phi - phi_i)
    )
    return base * sqrt(base)


@njit
def Bdot_numerators(R, R_i, theta, theta_i, phi, phi_i):
    n1 = -(
        R
        - R_i
        * (cos(theta) * cos(theta_i) + (sin(theta) * sin(theta_i * cos(phi - phi_i))))
    )
    n2 = (
        R
        * R_i
        * (-sin(theta) * cos(theta_i) + cos(theta) * sin(theta_i) * cos(phi - phi_i))
    )
    n3 = -R * R_i * sin(theta) * sin(theta_i) * sin(phi - phi_i)
    return (n1, n2, n3)
