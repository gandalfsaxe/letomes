"""
Equations related to the cartesian and spherical coordinate system.

* Get unit vectors
* Euclidian distances between two points
* Position coordinate conversions
* Velocity coordinate conversions
* Speed from position and velocity
"""

from math import acos, atan2, cos, pi, sin, sqrt

import numpy as np

from pprint import pprint


# region Distances
def get_distance_cartesian(u, v):
    """Get distance between two sets of cartesian coordinates by Pythagoras."""
    x1, y1, z1 = u
    x2, y2, z2 = v

    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def get_distance_spherical(u, v):
    """Get distance between two sets of spherical coordinates."""
    r1, theta1, phi1 = u
    r2, theta2, phi2 = v

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
    """
    Get cartesian (x,y,z) coordinates from spherical (r, theta, phi) coordinates,
    in the standard range r > 0, 0 < theta < pi, -pi< phi <= pi.

    Arguments:
        r {float} -- Radial coordinate (length of position vector)
        theta {float} -- Theta angle (rad), angle from z-axis to position vector.
        phi {float} -- Phi angle (rad), angle from a-axis to point projected to x-y
                       plane.

    Raises:
        ValueError -- r cannot be zero      (to ensure unique solution)
        ValueError -- theta cannot be zero  (to ensure unique solution)

    Returns:
        List[float] -- Cartesian [x, y, z] coordinates corresponding to spherical input
                       coordinates.
    """
    if r <= 0:
        raise ValueError("r cannot be less than or equal to zero.")
    if theta <= 0 or theta >= pi:
        raise ValueError("theta must be in range 0 < theta < pi.")
    if phi <= -pi or phi > pi:
        raise ValueError("phi must be in range -pi < phi <= pi.")

    x = r * sin(theta) * cos(phi)
    y = r * sin(theta) * sin(phi)
    z = r * cos(theta)

    return x, y, z


def get_position_spherical_from_cartesian(x, y, z):
    """Get spherical (r, theta, phi) coordinates from cartesian (x,y,z) coordinates"""
    if x == 0.0 and y == 0.0:
        raise ValueError(
            """
        x=0 and y=0 encountered; cartesian coordinate along z-axis results in
        indeterminate expression for (r,theta,phi).
        """
        )
    r = sqrt(x ** 2 + y ** 2 + z ** 2)
    theta = acos(z / r)
    phi = atan2(y, x)

    return r, theta, phi


# endregion


# region Velocity Coordinate Conversions
def get_velocity_spherical_from_cartesian(v, vdot):
    """
    Get velocity vector in spherical coordinates (rdot, thetadot, phidot)
    from cartesian coordinates.
    """
    x, y, z = v
    xdot, ydot, zdot = vdot

    if x == 0 and y == 0:
        raise ValueError("Position can't be on z-axis (x==0 and y==0).")

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


# region UNUSED AND UNTESTED
# ---Unit Vectors (Spherical)
# def get_unit_r_in_cartesian(theta, phi):
#     """Get spherical r unit vector in cartesian coordinates"""
#     R_hat = (
#         sin(theta) * cos(phi) * np.array([1, 0, 0])
#         + sin(theta) * sin(phi) * np.array([0, 1, 0])
#         + cos(theta) * np.array([0, 0, 1])
#     )

#     return R_hat


# def get_unit_theta_in_cartesian(theta, phi):
#     """Get spherical theta unit vector in cartesian coordinates"""
#     theta_hat = (
#         cos(theta) * cos(phi) * np.array([1, 0, 0])
#         + cos(theta) * sin(phi) * np.array([0, 1, 0])
#         - sin(theta) * np.array([0, 0, 1])
#     )

#     return theta_hat


# def get_unit_phi_in_cartesian(phi):
#     """Get spherical phi unit vector in cartesian coordinates"""
#     phi_hat = -sin(phi) * np.array([1, 0, 0]) + cos(phi) * np.array([0, 1, 0])

#     return phi_hat


# endregion

if __name__ == "__main__":
    # v = (1, 0, 0)
    # vdot = (0, 1, 0)

    # pprint(get_velocity_spherical_from_cartesian(v, vdot))
    pass
