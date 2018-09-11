"""
Functions for getting planets positions (ephemeris).
Will either get done via table or simulated elliptical orbits, whichever proves easier.
"""


def get_ephemeris(datetime):
    """
    Return ephemeris (e.g. positions) at datetime.
    All returned lists contain 3 elements:
        [0]: Sun
        [1]: Earth
        [2]: Mars
    R_ks, theta_ks, phi_ks are the spherical coordinates with Sun in origin.
    """
    R_ks, theta_ks, phi_ks = None, None, None

    return R_ks, theta_ks, phi_ks
