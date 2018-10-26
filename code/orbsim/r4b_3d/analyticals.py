"""
Equations of motion for R4B-3D system (Restricted 4-Body Problem in 3 Dimensions).
Derived via Hamiltons's equations.

1. `analyticals.py`: set up the equations of motion.

2. `integrators.py`: discretize the equations of motion and defines a single time step of the
    chosen numerical algorithm.

3. `simulators.py`: run the single steps from `integrators.py` repeatedly for some initial
    conditions and stopping conditions.
"""

import logging

# import logging
from math import acos, atan, cos, pi, sin, sqrt, tan, radians, degrees

import numpy as np

from orbsim.r4b_3d import (
    EARTH_RADIUS,
    ETA_EARTH,
    ETA_MARS,
    ETA_SUN,
    UNIT_LENGTH,
    UNIT_TIME,
    UNIT_VELOCITY,
)

from orbsim.r4b_3d.ephemerides import get_ephemerides

# from orbsim.r4b_3d.logging import logging_setup

eta_ks = [ETA_SUN, ETA_EARTH, ETA_MARS]

# from numba import njit


# level = logging.INFO

# logger = logging.getLogger()
# logger.setLevel(level)

# formatter = logging.Formatter("%(asctime)s - %(levelname)s (%(funcName)s): %(message)s")

# fh = logging.FileHandler("log_filename.txt")
# fh.setLevel(level)
# fh.setFormatter(formatter)
# logger.addHandler(fh)

# ch = logging.StreamHandler()
# ch.setLevel(level)
# ch.setFormatter(formatter)
# logger.addHandler(ch)

# @njit
def get_Rdot(B_r):
    """Rdot(R, theta, phi, B_r, B_theta, B_phi) from Hamilton's equations"""
    return B_r


# @njit
def get_thetadot(R, B_theta):
    """thetadot(R, theta, phi, B_r, B_theta, B_phi) from Hamilton's equations"""
    return B_theta / (R ** 2)


# @njit
def get_phidot(R, theta, B_phi):
    """phidot(R, theta, phi, B_r, B_theta, B_phi) from Hamilton's equations"""
    return B_phi / (R ** 2 * sin(theta) ** 2)


# @njit
def get_Bdot(R, theta, phi, B_theta, B_phi, R_ks, theta_ks, phi_ks):
    """
    All three Bdot from Hamilton's equations (Bdot_r, Bdot_theta and Bdot_phi)
    """
    # Initialize Bdot parts
    Bdot_r1 = B_theta ** 2 / (R ** 3)
    Bdot_r2 = B_phi ** 2 / (R ** 3 * sin(theta) ** 2)
    Bdot_r3 = 0
    Bdot_theta1 = B_phi ** 2 / (R ** 2 * sin(theta) ** 2 * tan(theta))
    Bdot_theta2 = 0
    Bdot_phi1 = 0
    # Everything under the summation
    for i, _ in enumerate(R_ks):
        numerator_1, numerator_2, numerator_3 = Bdot_numerators(
            R, theta, phi, R_ks[i], theta_ks[i], phi_ks[i]
        )
        denominator = Bdot_denominator(R, theta, phi, R_ks[i], theta_ks[i], phi_ks[i])
        Bdot_r3 += eta_ks[i] * numerator_1 / denominator
        Bdot_theta2 += eta_ks[i] * numerator_2 / denominator
        Bdot_phi1 += eta_ks[i] * numerator_3 / denominator
    # Add Bdot parts
    Bdot_r = Bdot_r1 + Bdot_r2 + Bdot_r3
    Bdot_theta = Bdot_theta1 + Bdot_theta2
    Bdot_phi = Bdot_phi1
    return Bdot_r, Bdot_theta, Bdot_phi


# @njit
def Bdot_denominator(R, theta, phi, R_k, theta_k, phi_k):
    """fraction denominator for generalized momenta Bdot"""
    base = (R - R_k) ** 2 * (
        cos(theta) * cos(theta_k) + sin(theta) * sin(theta_k) * cos(phi - phi_k)
    )

    return base * sqrt(base)


# @njit
def Bdot_numerators(R, theta, phi, R_k, theta_k, phi_k):
    """fraction numerators for generalized momenta Bdot"""
    n1 = -(
        R
        - R_k
        * (cos(theta) * cos(theta_k) + (sin(theta) * sin(theta_k * cos(phi - phi_k))))
    )
    n2 = (
        R
        * R_k
        * (-sin(theta) * cos(theta_k) + cos(theta) * sin(theta_k) * cos(phi - phi_k))
    )
    n3 = -R * R_k * sin(theta) * sin(theta_k) * sin(phi - phi_k)
    return (n1, n2, n3)


# TODO: Region


def get_B_R(Rdot):
    return Rdot


def get_B_theta(R, thetadot):
    return R ** 2 * thetadot


def get_B_phi(R, theta, phidot):
    return R ** 2 * sin(theta) ** 2 * phidot


def get_unit_R(theta, phi):
    R_hat = (
        sin(theta) * cos(phi) * np.array([1, 0, 0])
        + sin(theta) * sin(phi) * np.array([0, 1, 0])
        + cos(theta) * np.array([0, 0, 1])
    )

    return R_hat


def get_unit_theta(theta, phi):
    theta_hat = (
        cos(theta) * cos(phi) * np.array([1, 0, 0])
        + cos(theta) * sin(phi) * np.array([0, 1, 0])
        - sin(theta) * np.array([0, 0, 1])
    )

    return theta_hat


def get_unit_phi(phi):
    phi_hat = -sin(phi) * np.array([1, 0, 0]) + cos(phi) * np.array([0, 1, 0])

    return phi_hat


# TODO: Region


def get_position_cartesian(r, theta, phi):
    """Get cartesian (x,y,z) coordinates from spherical (r, theta, phi) coordinates"""
    x = r * sin(theta) * cos(phi)
    y = r * sin(theta) * sin(phi)
    z = r * cos(theta)

    return x, y, z


def get_position_spherical(x, y, z):
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


def get_velocity_spherical(x, y, z, xdot, ydot, zdot):

    rdot = (x * xdot + y * ydot + z * zdot) / (sqrt(x ** 2 + y ** 2 + z ** 2))

    thetadot = ((x * xdot + y * ydot) * z - (x ** 2 + y ** 2) * zdot) / (
        (x ** 2 + y ** 2 + z ** 2) * sqrt(x ** 2 + y ** 2)
    )

    phidot = (x * ydot - xdot * y) / (x ** 2 + y ** 2)

    return (rdot, thetadot, phidot)


def get_speed_spherical(r, theta, rdot, thetadot, phidot):
    """Get speed of body given in spherical coordinates."""
    v = sqrt(
        rdot ** 2 + r ** 2 * thetadot ** 2 + r ** 2 * sin(theta) ** 2 * phidot ** 2
    )

    return v


def get_leo_speed(altitude=160):
    """ Get speed of LEO (Low Earth Orbit) at designated altitude.

    Keyword Arguments:
        altitude {int} -- distance above Earth surface in km (default: {100})

    Returns:
        [int] -- speed in km/s.
    """

    v = sqrt(ETA_EARTH / ((EARTH_RADIUS + altitude) / UNIT_LENGTH))

    v_kmps = v * UNIT_LENGTH / UNIT_TIME

    logging.debug(
        f"Initial LEO orbital speed at {altitude} km altitude (geocentric, AU/y): {v}"
        f" (Expected: 1.6468 au/y (via Wolfram Alpha))"
        # https://www.wolframalpha.com/input/?i=7.812+km%2Fs+in+au%2Fy
    )
    logging.debug(
        f"Initial LEO orbital speed at {altitude} km altitude (geocentric, km/s): "
        f"{v_kmps}"
        f" (Expected: 7.812 km/s (via Wolfram Alpha))"
        # https://www.wolframalpha.com/input/?i=circular+orbital+speed+earth+altitude+160km
    )

    return v_kmps


def get_leo_period(altitude=160):
    """ Get period of LEO (Low Earth Orbit) at designated altitude.

    Keyword Arguments:
        altitude {int} -- distance above Earth surface in km (default: {100})

    Returns:
        [int] -- time in s.
    """

    T = 2 * pi * sqrt((EARTH_RADIUS + altitude) ** 3 / ETA_EARTH)

    logging.debug(
        f"Initial LEO orbital period at {altitude} km altitude (s): {T}"
        f"(Expected: 5261 s (via Wolfram Alpha)"
    )
    # https://www.wolframalpha.com/input/?i=circular+orbital+period+earth+altitude+160km

    logging.debug(
        f"Initial LEO orbital period at {altitude} km altitude (hours): {T/3600}"
        f"(Expected: 1.461 h  (Via Wolfram Alpha)"
    )
    # https://www.wolframalpha.com/input/?i=circular+orbital+period+earth+altitude+160km

    return T


def get_leo_position_and_velocity(ephemerides, day, altitude=160):
    """Calculate direction of initial velocity vector.
    Assumes ephemerides are given with 1 day interval. With a series of cross products,
    calculate a LEO position perpendicular and velocity parallel to Earth's velocity
    vector in same direction and plane as Earth.

    Arguments:
        ephemerides {[dict of pandas dataframe]} -- ephemerides table.
        day {[int]} -- day (day=0 at 2019-01-01 00:00:00)

    Keyword Arguments:
        orientation {str} -- Wanted LEO orbit orientation (default: {'ecliptic'})

    Returns:
        List[List[int]] -- Initial LEO position vector, spherical [AU/y, rad, rad]
                           initial LEO velocity vector, spherical [AU/y, rad/y, rad/y]
    """

    # ---------- 1 Calculate Earth velocity and speed (cartesian & spherical)

    # Earth velocity at day = dr/dt ≈ Δr/Δt, where Δt = 1 day
    # i.e. Earth velocity estimated by difference of position vector 1 day apart / 1 day
    earth_day = ephemerides["earth"].iloc[day]
    earth_daym1 = ephemerides["earth"].iloc[day - 1]
    earth_diff = earth_day - earth_daym1

    # Get positions of Earth at {day, day-1} in spherical and cartesian coordinates
    earth_q0_spherical_AU = [earth_day["r"], earth_day["theta"], earth_day["phi"]]
    earth_q0_cartesian_AU = [earth_day["x"], earth_day["y"], earth_day["z"]]

    earth_qm1_spherical_AU = [
        earth_daym1["r"],
        earth_daym1["theta"],
        earth_daym1["phi"],
    ]
    earth_qm1_cartesian_AU = [earth_daym1["x"], earth_daym1["y"], earth_daym1["z"]]

    # Average r and theta needed for speed computation in spherical coordinates
    r_average_AU = np.mean([earth_day["r"], earth_daym1["r"]])
    r_average_km = r_average_AU * UNIT_LENGTH
    logging.debug(f"r_average: {r_average_AU} AU = {r_average_km} km")

    theta_average_deg = np.mean([earth_day["theta"], earth_daym1["theta"]])
    theta_average_rad = radians(theta_average_deg)
    logging.debug(f"theta_average: {theta_average_deg} deg = {theta_average_rad} rad")

    # Earth velocity vector in spherical and cartesian coordinates and convert units
    earth_qdot0_spherical_au_day_deg = [
        earth_diff["r"],
        earth_diff["theta"],
        earth_diff["phi"],
    ]

    earth_qdot0_spherical_km_s_rad = [
        earth_qdot0_spherical_au_day_deg[0] / (24 * 3600) * UNIT_LENGTH,
        radians(earth_qdot0_spherical_au_day_deg[1]) / (24 * 3600),
        radians(earth_qdot0_spherical_au_day_deg[2]) / (24 * 3600),
    ]

    earth_qdot0_cartesian_au_day = [earth_diff["x"], earth_diff["y"], earth_diff["z"]]

    earth_qdot0_cartesian_km_s = [
        earth_qdot0_cartesian_au_day[0] / (24 * 3600) * UNIT_LENGTH,
        earth_qdot0_cartesian_au_day[1] / (24 * 3600) * UNIT_LENGTH,
        earth_qdot0_cartesian_au_day[2] / (24 * 3600) * UNIT_LENGTH,
    ]

    # Speeds
    earth_qdot0_spherical_km_s_rad_speed = get_speed_spherical(
        r_average_km,
        theta_average_rad,
        earth_qdot0_spherical_km_s_rad[0],  # rdot
        earth_qdot0_spherical_km_s_rad[1],  # thetadot
        earth_qdot0_spherical_km_s_rad[2],  # phidot
    )

    earth_qdot0_cartesian_au_day_speed = np.linalg.norm(earth_qdot0_cartesian_au_day)

    earth_qdot0_cartesian_km_s_speed = np.linalg.norm(earth_qdot0_cartesian_km_s)

    # Logs
    logging.debug(
        f"Earth initial position at day {day} (cartesian): {earth_q0_cartesian_AU}"
    )
    logging.debug(
        f"Earth initial position at day {day-1} (cartesian): {earth_qm1_cartesian_AU}"
    )

    logging.debug(
        f"Earth initial position at day {day} (spherical): {earth_q0_spherical_AU}"
    )
    logging.debug(
        f"Earth initial position at day {day-1} (spherical): {earth_qm1_spherical_AU}"
    )

    logging.debug(
        f"Earth initial velocity (spherical, AU/d & deg/d): {earth_qdot0_spherical_au_day_deg}"
    )
    logging.debug(
        f"Earth initial velocity (spherical, km/s & rad/s): {earth_qdot0_spherical_km_s_rad}"
        f" (speed: {earth_qdot0_spherical_km_s_rad_speed})"
    )

    logging.debug(
        f"Earth initial velocity (cartesian, AU/d): {earth_qdot0_cartesian_au_day}"
        f" (speed: {earth_qdot0_cartesian_au_day_speed})"
    )
    logging.debug(
        f"Earth initial velocity (cartesian, km/s): {earth_qdot0_cartesian_km_s}"
        f"        (speed: {earth_qdot0_cartesian_km_s_speed})"
    )

    # ---------- 2 Earth plane vector

    earth_orbital_plane = np.cross(earth_q0_cartesian_AU, earth_qdot0_cartesian_au_day)
    earth_orbital_plane /= np.linalg.norm(earth_orbital_plane)

    logging.debug(f"Ecliptic plane vector: {earth_orbital_plane}")

    # ---------- 3 Spacecraft initial position

    # Spacecraft geocentric position: perpendicular to earth velocity pointing outwards
    q0_geocentric_cartesian_unit = np.cross(earth_q0_cartesian_AU, earth_orbital_plane)
    q0_geocentric_cartesian_unit /= np.linalg.norm(q0_geocentric_cartesian_unit)

    q0_geocentric_cartesian_km = q0_geocentric_cartesian_unit * (
        EARTH_RADIUS + altitude
    )

    q0_geocentric_cartesian_AU = q0_geocentric_cartesian_km / UNIT_LENGTH
    q0_cartesian_AU = earth_q0_cartesian_AU + q0_geocentric_cartesian_AU
    q0_cartesian_km = q0_cartesian_AU * UNIT_LENGTH

    q0_spherical_AU_rad = list(get_position_spherical(*q0_cartesian_AU))

    q0_spherical_AU_deg = list(q0_spherical_AU_rad)  # copy, not reference
    q0_spherical_AU_deg[1] = degrees(q0_spherical_AU_deg[1])
    q0_spherical_AU_deg[2] = degrees(q0_spherical_AU_deg[2])

    logging.debug(
        f"Spacecraft initial position unit vector (geocentric, cartesian): "
        f"{q0_geocentric_cartesian_unit}"
    )

    logging.debug(
        f"Spacecraft initial position (geocentric, cartesian, km): "
        f"{q0_geocentric_cartesian_km}"
        f" (distance from Earth center: {np.linalg.norm(q0_geocentric_cartesian_km)})"
    )

    logging.debug(
        f"Spacecraft initial position (geocentric, cartesian, AU): "
        f"{q0_geocentric_cartesian_AU}"
        f" (distance from Earth center: {np.linalg.norm(q0_geocentric_cartesian_AU)})"
    )
    logging.debug(
        f"Spacecraft initial position (heliocentric, cartesian, AU): "
        f"{q0_cartesian_AU}"
    )
    logging.debug(
        f"Spacecraft initial position (heliocentric, cartesian, km): "
        f"{q0_cartesian_km}"
    )

    logging.debug(
        f"Spacecraft initial position (heliocentric, spherical, AU & rad): "
        f"{q0_spherical_AU_rad}"
    )
    logging.debug(
        f"Spacecraft initial position (heliocentric, spherical, AU & deg): "
        f"{q0_spherical_AU_deg}"
    )

    # ---------- 4 Spacecraft initial velocity
    # Spacecraft velocity = Earth velocity + leo speed (same direction as Earth)

    leo_speed = get_leo_speed(altitude)

    qdot0_cartesian_unit = list(earth_qdot0_cartesian_km_s)
    qdot0_cartesian_unit /= np.linalg.norm(qdot0_cartesian_unit)

    qdot0_cartesian_km_s = earth_qdot0_cartesian_km_s + qdot0_cartesian_unit * leo_speed
    qdot0_cartesian_km_s_speed = np.linalg.norm(qdot0_cartesian_km_s)

    # Get spherical velocity vector from cartesian velocity vector
    qdot0_spherical_km_s_rad = get_velocity_spherical(
        *q0_cartesian_km, *qdot0_cartesian_km_s
    )

    qdot0_spherical_km_s_rad_speed = get_speed_spherical(
        r_average_km,
        theta_average_rad,
        qdot0_spherical_km_s_rad[0],  # rdot
        qdot0_spherical_km_s_rad[1],  # thetadot
        qdot0_spherical_km_s_rad[2],  # phidot
    )

    qdot0_spherical_AU_rad_year = [
        qdot0_spherical_km_s_rad[0] / UNIT_VELOCITY,  # AU/y
        qdot0_spherical_km_s_rad[1] * UNIT_TIME,  # rad/y
        qdot0_spherical_km_s_rad[2] * UNIT_TIME,  # rad/y
    ]

    qdot0_spherical_AU_rad_year_speed = get_speed_spherical(
        r_average_AU,
        theta_average_rad,
        qdot0_spherical_AU_rad_year[0],  # rdot
        qdot0_spherical_AU_rad_year[1],  # thetadot
        qdot0_spherical_AU_rad_year[2],  # phidot
    )

    logging.debug(
        f"Spacecraft initial velocity unit vector (cartesian, km/s): "
        f"{qdot0_cartesian_unit}"
    )
    logging.debug(
        f"Spacecraft initial velocity vector (cartesian, km/s): {qdot0_cartesian_km_s}"
        f" (speed: {qdot0_cartesian_km_s_speed})"
    )

    logging.debug(
        f"Spacecraft initial velocity vector (spherical, km/s & rad/s): "
        f"{qdot0_spherical_km_s_rad}"
        f" (speed: {qdot0_spherical_km_s_rad_speed})"
    )

    logging.debug(
        f"Spacecraft initial velocity vector (spherical, AU/y & rad/y (dimless)): "
        f"{qdot0_spherical_AU_rad_year}"
        f" (speed: {qdot0_spherical_AU_rad_year_speed})"
    )

    # Repeat logging but as info instead of debug
    logging.info(
        f"Spacecraft initial position vector (spherical, AU & rad (dimless)): "
        f"{q0_spherical_AU_rad}"
    )
    logging.info(
        f"Spacecraft initial velocity vector (spherical, AU/y & rad/y (dimless)): "
        f"{qdot0_spherical_AU_rad_year}"
        f" (speed: {qdot0_spherical_AU_rad_year_speed})"
    )

    return q0_spherical_AU_rad, qdot0_spherical_AU_rad_year


if __name__ == "__main__":

    # logging_setup("info")

    ephemerides = get_ephemerides()

    leo = get_leo_position_and_velocity(ephemerides, day=0)

    # logging.info(f"LEO (position, velocity), cartesian, AU: {leo}")

    # t90p0 = get_unit_R(theta=pi / 2, phi=0)
    # print(f"t90p0: {t90p0}")
    # t90p90 = get_unit_R(theta=pi / 2, phi=pi / 2)
    # print(f"t90p90: {t90p90}")
    # t0p0 = get_unit_R(theta=0, phi=0)
    # print(f"t0p0: {t0p0}")

    # t0p0 = get_unit_theta(theta=0, phi=0)
    # print(f"t0p0: {t0p0}")
    # t180p0 = get_unit_theta(theta=pi, phi=0)
    # print(f"t180p0: {t180p0}")
    # t180pm90 = get_unit_theta(theta=pi, phi=-pi / 2)
    # print(f"t180pm90: {t180pm90}")
    # t180p90 = get_unit_theta(theta=pi, phi=pi / 2)
    # print(f"t180p90: {t180p90}")
    # t90p0 = get_unit_theta(theta=pi / 2, phi=0)
    # print(f"t90p0: {t90p0}")

    # t90pm90 = get_unit_phi(theta=pi / 2, phi=-pi / 2)
    # print(f"t90pm90: {t90pm90}")
    # t90p90 = get_unit_phi(theta=pi / 2, phi=pi / 2)
    # print(f"t90p90: {t90p90}")
    # t90p0 = get_unit_phi(theta=pi / 2, phi=0)
    # print(f"t90p0: {t90p0}")
    # t90p180 = get_unit_phi(theta=pi / 2, phi=pi)
    # print(f"t90p180: {t90p180}")

    # pass
