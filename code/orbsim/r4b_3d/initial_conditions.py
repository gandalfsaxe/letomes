"""Functions that calculate various useful initial conditions for the R4B simulator."""

import logging
from math import degrees, radians

import numpy as np

from orbsim import EARTH_RADIUS, SUN_RADIUS
from orbsim.r4b_3d import UNIT_LENGTH, UNIT_TIME, UNIT_VELOCITY
from orbsim.r4b_3d.coordinate_system import (
    get_position_spherical_from_cartesian,
    get_speed_spherical,
    get_velocity_spherical_from_cartesian,
)
from orbsim.r4b_3d.ephemerides import get_ephemerides, get_ephemerides_on_day
from orbsim.r4b_3d.equations_of_physics import get_circular_orbit_speed

from orbsim.r4b_3d.equations_of_motion import get_B_R, get_B_theta, get_B_phi


def get_leo_position_and_velocity(day=0, altitude=160, end_year="2020"):
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
    ephemerides = get_ephemerides(end_year=end_year)
    eph_day = get_ephemerides_on_day(ephemerides, day)
    eph_daym1 = get_ephemerides_on_day(ephemerides, day - 1)

    earth_day = eph_day["earth"]
    earth_daym1 = eph_daym1["earth"]
    earth_diff = earth_day - earth_daym1

    # Get positions of Earth at {day, day-1} in spherical and cartesian coordinates
    earth_q0_spherical_AU_deg = [earth_day["r"], earth_day["theta"], earth_day["phi"]]
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
        f"Earth initial position at day {day} (cartesian, AU): "
        f"{earth_q0_cartesian_AU}"
    )
    logging.debug(
        f"Earth initial position at day {day-1} (cartesian, AU): "
        f"{earth_qm1_cartesian_AU}"
    )

    logging.debug(
        f"Earth initial position at day {day} (spherical, AU & deg): "
        f"{earth_q0_spherical_AU_deg}"
    )
    logging.debug(
        f"Earth initial position at day {day-1} (spherical, AU & deg): "
        f"{earth_qm1_spherical_AU}"
    )

    logging.debug(
        f"Earth initial velocity (spherical, AU/d & deg/d): "
        f"{earth_qdot0_spherical_au_day_deg}"
    )
    logging.debug(
        f"Earth initial velocity (spherical, km/s & rad/s): "
        f"{earth_qdot0_spherical_km_s_rad} "
        f"(speed: {earth_qdot0_spherical_km_s_rad_speed})"
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
    # (i.e. chosen such that it's the one pointing outwards from elliptical orbit)
    # (note this means spacecraft speed != earth speed (helio) + spacecraft speed (geo))
    q0_geocentric_cartesian_unit = np.cross(
        earth_qdot0_cartesian_km_s, earth_orbital_plane
    )
    q0_geocentric_cartesian_unit /= np.linalg.norm(q0_geocentric_cartesian_unit)

    q0_geocentric_cartesian_km = q0_geocentric_cartesian_unit * (
        EARTH_RADIUS + altitude
    )
    q0_geocentric_cartesian_AU = q0_geocentric_cartesian_km / UNIT_LENGTH

    q0_cartesian_AU = earth_q0_cartesian_AU + q0_geocentric_cartesian_AU
    q0_cartesian_km = q0_cartesian_AU * UNIT_LENGTH

    q0_spherical_AU_rad = list(get_position_spherical_from_cartesian(*q0_cartesian_AU))

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

    leo_speed = get_circular_orbit_speed("Earth", altitude)

    qdot0_cartesian_unit = list(earth_qdot0_cartesian_km_s)
    qdot0_cartesian_unit /= np.linalg.norm(qdot0_cartesian_unit)

    qdot0_cartesian_km_s = earth_qdot0_cartesian_km_s + qdot0_cartesian_unit * leo_speed
    qdot0_cartesian_km_s_speed = np.linalg.norm(qdot0_cartesian_km_s)

    # Get spherical velocity vector from cartesian velocity vector
    qdot0_spherical_km_s_rad = get_velocity_spherical_from_cartesian(
        q0_cartesian_km, qdot0_cartesian_km_s
    )

    qdot0_spherical_km_s_rad_speed = get_speed_spherical(
        r_average_km,
        theta_average_rad,
        qdot0_spherical_km_s_rad[0],  # rdot
        qdot0_spherical_km_s_rad[1],  # thetadot
        qdot0_spherical_km_s_rad[2],  # phidot
    )

    qdot0_spherical_AU_rad_y = [
        qdot0_spherical_km_s_rad[0] / UNIT_VELOCITY,  # AU/y
        qdot0_spherical_km_s_rad[1] * UNIT_TIME,  # rad/y
        qdot0_spherical_km_s_rad[2] * UNIT_TIME,  # rad/y
    ]

    qdot0_spherical_AU_rad_year_speed = get_speed_spherical(
        r_average_AU,
        theta_average_rad,
        qdot0_spherical_AU_rad_y[0],  # rdot
        qdot0_spherical_AU_rad_y[1],  # thetadot
        qdot0_spherical_AU_rad_y[2],  # phidot
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
        f"Spacecraft initial velocity vector (spherical, AU/y & rad/y): "
        f"{qdot0_spherical_AU_rad_y}"
        f" (speed: {qdot0_spherical_AU_rad_year_speed})"
    )

    # FINAL OUTPUT: Initial coordinates (Q)
    Q0 = q0_spherical_AU_rad

    # FINAL OUTPUT: Initial momenta per mass (B)
    R, theta, _ = Q0
    Rdot, thetadot, phidot = qdot0_spherical_AU_rad_y

    B_R = get_B_R(Rdot)
    B_theta = get_B_theta(R, thetadot)
    B_phi = get_B_phi(R, theta, phidot)

    B0 = [B_R, B_theta, B_phi]

    # Info log output
    logging.info(
        f"Spacecraft initial position vector, Q0 (spherical, AU & rad): " f"{Q0}"
    )
    logging.info(
        f"Spacecraft initial momentum per mass vector, B0 (AU/y & rad/y): {B0}"
    )

    return Q0, B0


def get_circular_sun_orbit_position_and_velocity(altitude=UNIT_LENGTH - SUN_RADIUS):
    """Get orbit speed for circular orbit around the at altitude.

    Keyword Arguments:
        altitude {float} -- Altitude above Sun surface (km)
                            (default: {UNIT_LENGTH-SUN_RADIUS})

    Returns:
        float -- Required orbit speed for circular orbit around sun (km/s)
    """

    sun_orbital_speed = get_circular_orbit_speed(body="Sun", altitude=altitude)

    logging.debug(
        f"Required orbital speed at altitude {altitude:.2f} km above Sun: "
        f"{sun_orbital_speed} km/s"
    )

    # Position
    q0_cartesian_AU = [1, 0, 0]
    q0_cartesian_km = [q * UNIT_LENGTH for q in q0_cartesian_AU]
    q0_spherical_AU_rad = get_position_spherical_from_cartesian(*q0_cartesian_AU)

    logging.debug(f"Position (heliocentric, cartesian, AU: {q0_cartesian_AU}")
    logging.debug(f"Position (heliocentric, cartesian, km: {q0_cartesian_km}")
    logging.debug(f"Position (heliocentric, spherical, AU & rad: {q0_spherical_AU_rad}")

    # Velocity
    qdot0_cartesian_km_s = [0, sun_orbital_speed, 0]
    qdot0_cartesian_AU_y = [v_i / UNIT_VELOCITY for v_i in qdot0_cartesian_km_s]
    qdot0_spherical_AU_rad_y = get_velocity_spherical_from_cartesian(
        q0_cartesian_AU, qdot0_cartesian_AU_y
    )

    logging.debug(f"Velocity (heliocentric, cartesian, km/s: {qdot0_cartesian_km_s}")
    logging.debug(f"Velocity (heliocentric, cartesian, AU/y: {qdot0_cartesian_AU_y}")
    logging.debug(
        f"Velocity (heliocentric, spherical, AU/y & rad/y: {qdot0_spherical_AU_rad_y}"
    )

    # FINAL OUTPUT: Initial coordinates (Q)
    Q0 = q0_spherical_AU_rad

    # FINAL OUTPUT: Initial momenta per mass (B)
    R, theta, _ = Q0
    Rdot, thetadot, phidot = qdot0_spherical_AU_rad_y

    B_R = get_B_R(Rdot)
    B_theta = get_B_theta(R, thetadot)
    B_phi = get_B_phi(R, theta, phidot)

    B0 = [B_R, B_theta, B_phi]

    # Info log output
    logging.info(
        f"Spacecraft initial position vector, Q0 (spherical, AU & rad): " f"{Q0}"
    )
    logging.info(
        f"Spacecraft initial momentum per mass vector, B0 (AU/y & rad/y): {B0}"
    )

    return Q0, B0


if __name__ == "__main__":

    from orbsim.r4b_3d.logging import logging_setup

    logging_setup()

    #     # get_leo_position_and_velocity()

    get_circular_sun_orbit_position_and_velocity()
