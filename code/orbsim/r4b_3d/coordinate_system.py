"""
Equations related to the cartesian and spherical coordinate system.

* Get unit vectors
* Euclidian distances between two points
* Position coordinate conversions
* Velocity coordinate conversions
* Speed from position and velocity
"""

from math import acos, atan, cos, pi, sin, sqrt

import numpy as np


# region Unit Vectors (Spherical)
def get_unit_r_in_cartesian(theta, phi):
    """Get spherical r unit vector in cartesian coordinates"""
    R_hat = (
        sin(theta) * cos(phi) * np.array([1, 0, 0])
        + sin(theta) * sin(phi) * np.array([0, 1, 0])
        + cos(theta) * np.array([0, 0, 1])
    )

    return R_hat


def get_unit_theta_in_cartesian(theta, phi):
    """Get spherical theta unit vector in cartesian coordinates"""
    theta_hat = (
        cos(theta) * cos(phi) * np.array([1, 0, 0])
        + cos(theta) * sin(phi) * np.array([0, 1, 0])
        - sin(theta) * np.array([0, 0, 1])
    )

    return theta_hat


def get_unit_phi_in_cartesian(phi):
    """Get spherical phi unit vector in cartesian coordinates"""
    phi_hat = -sin(phi) * np.array([1, 0, 0]) + cos(phi) * np.array([0, 1, 0])

    return phi_hat


# endregion

# region Distances
def get_distance_cartesian(x1, y1, z1, x2, y2, z2):
    """Get distance between two sets of cartesian coordinates by Pythagoras."""
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def get_distance_spherical(r1, theta1, phi1, r2, theta2, phi2):
    """Get distance between two sets of spherical coordinates."""
    return sqrt(
        r1 ** 2
        + r2 ** 2
        - 2
        * r1
        * r2
        * (
            cos(theta1) * cos(theta2)
            + sin(theta1)
            * sin(theta2)
            * (cos(phi1) * cos(phi2) + sin(phi1) * sin(phi2))
        )
    )


# endregion


# region Position Coordinate Conversions
def get_position_cartesian_from_spherical(r, theta, phi):
    """Get cartesian (x,y,z) coordinates from spherical (r, theta, phi) coordinates"""
    x = r * sin(theta) * cos(phi)
    y = r * sin(theta) * sin(phi)
    z = r * cos(theta)

    return x, y, z


def get_position_spherical_from_cartesian(x, y, z):
    """Get spherical (r, theta, phi) coordinates from cartesian (x,y,z) coordinates"""
    r = sqrt(x ** 2 + y ** 2 + z ** 2)
    theta = acos(z / r)
    if x >= 0:
        phi = atan(y / x)
    elif y >= 0:
        phi = atan(y / x) + pi
    else:
        phi = atan(y / x) - pi

    return r, theta, phi


# endregion


# region Velocity Coordinate Conversions
def get_velocity_spherical_from_cartesian(x, y, z, xdot, ydot, zdot):
    """
    Get velocity vector in spherical coordinates (rdot, thetadot, phidot)
    from cartesian coordinates.
    """

    rdot = (x * xdot + y * ydot + z * zdot) / (sqrt(x ** 2 + y ** 2 + z ** 2))

    thetadot = ((x * xdot + y * ydot) * z - (x ** 2 + y ** 2) * zdot) / (
        (x ** 2 + y ** 2 + z ** 2) * sqrt(x ** 2 + y ** 2)
    )

    phidot = (x * ydot - xdot * y) / (x ** 2 + y ** 2)

    return (rdot, thetadot, phidot)


# endregion

# region Speeds
def get_speed_spherical(r, theta, rdot, thetadot, phidot):
    """Get speed of body given in spherical coordinates."""
    v = sqrt(
        rdot ** 2 + r ** 2 * thetadot ** 2 + r ** 2 * sin(theta) ** 2 * phidot ** 2
    )

    return v


def get_speed_cartesian(xdot, ydot, zdot):
    """Get speed of body given in cartesian coordinates."""
    v = sqrt(xdot ** 2 + ydot ** 2 + zdot ** 2)

    return v


# endregion
