"""Functions that calculate various useful initial conditions for the R4B simulator."""

import logging
from math import degrees, radians, floor, pi

import numpy as np
from numpy import cos, sin, sqrt, tan

from orbsim import EARTH_RADIUS, SUN_RADIUS, DAY
from orbsim.r4b_3d import UNIT_LENGTH, UNIT_TIME, UNIT_VELOCITY
from orbsim.r4b_3d.coordinate_system import (
    get_position_spherical_from_cartesian,
    get_position_cartesian_from_spherical,
    get_speed_spherical,
    get_speed_cartesian,
    get_velocity_spherical_from_cartesian,
    get_distance_spherical
)
from new_ephemerides import get_ephemerides, get_ephemerides_on_day
from orbsim.r4b_3d.equations_of_physics import get_circular_orbit_speed

from orbsim.r4b_3d.equations_of_motion import get_B_R, get_B_theta, get_B_phi

from ctypes import *

cudasim = cdll.LoadLibrary("./libcudasim.so")

def rotate(v, k, theta):
    cos_theta = cos(theta)
    sin_theta = sin(theta)

    rotated = (v * cos_theta) + (np.cross(k, v) * sin_theta) + (k * np.dot(k, v)) * (1 - cos_theta)
    return rotated

def get_leo_positions_and_velocities(days=[0], burndvs=[0], tilts=[0], h = 0.1 / UNIT_TIME, altitude=160, max_year="2020"):
    hday = h * UNIT_TIME / DAY;
    earth_aphelion_AU = 1.0167
    earth_perihelion_AU = 0.98329
    #days[1] = 365.256363004

    #earth_a_AU = (earth_aphelion_AU + earth_perihelion_AU) / 2
    #earth_f_AU = earth_aphelion_AU - earth_a_AU
    #earth_b_AU = sqrt(earth_a_AU * earth_a_AU - earth_f_AU * earth_f_AU)

    ephemerides = get_ephemerides(max_year=max_year)

    day0s = np.zeros((len(days) * len(burndvs) * len(tilts)))
    Q0s = np.zeros((len(days) * len(burndvs) * len(tilts), 3))
    B0s = np.zeros((len(days) * len(burndvs) * len(tilts), 3))

    for n in range(len(days) * len(burndvs) * len(tilts)):

        i = int(floor(n / (len(burndvs) * len(tilts))))
        m = n % (len(burndvs) * len(tilts))
        j = int(floor(m / len(tilts)))
        k = m % len(tilts)

        day0s[n] = days[i]

        eph_day = get_ephemerides_on_day(ephemerides, days[i])

        sun_day = eph_day["sun"]
        s_spherical = np.array([sun_day["r"], radians(sun_day["theta"]), radians(sun_day["phi"])])

        mars_day = eph_day["mars"]
        m_spherical = np.array([mars_day["r"], radians(mars_day["theta"]), radians(mars_day["phi"])])

        earth_day = eph_day["earth"]
        e_spherical = np.array([earth_day["r"], radians(earth_day["theta"]), radians(earth_day["phi"])])
        e_cartesian = np.array(get_position_cartesian_from_spherical(e_spherical[0], e_spherical[1], e_spherical[2]))
        e_cartesian_unit = e_cartesian / np.linalg.norm(e_cartesian)

        eph_day0 = get_ephemerides_on_day(ephemerides, floor(days[i]))
        earth_day0 = eph_day0["earth"]
        e_cartesian0 = np.array([earth_day0["x"], earth_day0["y"], earth_day0["z"]])

        eph_day1 = get_ephemerides_on_day(ephemerides, floor(days[i] + 1))
        earth_day1 = eph_day1["earth"]
        e_cartesian1 = np.array([earth_day1["x"], earth_day1["y"], earth_day1["z"]])

        ev_cartesian = (e_cartesian1 - e_cartesian0) * UNIT_TIME / DAY
        ev_cartesian_unit = ev_cartesian / np.linalg.norm(ev_cartesian)
        ev_spherical = np.array(get_velocity_spherical_from_cartesian(e_cartesian, ev_cartesian))

        e_orbital_plane_cartesian = np.cross(e_cartesian, ev_cartesian)
        e_orbital_plane_cartesian /= np.linalg.norm(e_orbital_plane_cartesian)


        c_leo_cartesian = -1.0 * np.cross(e_orbital_plane_cartesian, ev_cartesian)
        c_leo_cartesian_unit = c_leo_cartesian / np.linalg.norm(c_leo_cartesian)

        c_cartesian = c_leo_cartesian_unit * (EARTH_RADIUS + altitude) / UNIT_LENGTH + e_cartesian
        c_spherical = np.array(get_position_spherical_from_cartesian(c_cartesian[0], c_cartesian[1], c_cartesian[2]))

        e_speed = UNIT_VELOCITY * get_speed_cartesian(ev_cartesian[0], ev_cartesian[1], ev_cartesian[2])
        leo_speed = get_circular_orbit_speed("Earth", altitude)
        burn_speed = burndvs[j]
        #cv_cartesian = (ev_cartesian_unit * (e_speed + leo_speed)) / UNIT_VELOCITY

        leo_cartesian_unit = rotate(ev_cartesian_unit, c_leo_cartesian_unit, tilts[k])
        burn_cartesian_unit = rotate(ev_cartesian_unit, e_orbital_plane_cartesian, 0)
        burn_cartesian = burn_cartesian_unit * burndvs[j] / UNIT_VELOCITY
        #cv_spherical_unit = np.array(get_position_spherical_from_cartesian(ev_cartesian_unit[0], ev_cartesian_unit[1], ev_cartesian_unit[2]))
        #cv_cartesian_unit = np.array(get_position_cartesian_from_spherical(cv_spherical_unit[0], cv_spherical_unit[1], cv_spherical_unit[2]))

        cv_cartesian = (ev_cartesian_unit * e_speed + 
                        leo_cartesian_unit * leo_speed +
                        leo_cartesian_unit * burndvs[j]) / UNIT_VELOCITY
        c_speed = UNIT_VELOCITY * get_speed_cartesian(cv_cartesian[0], cv_cartesian[1], cv_cartesian[2])
        cv_spherical = np.array(get_velocity_spherical_from_cartesian(c_cartesian, cv_cartesian))

        """

        c_spherical = np.array([e_spherical[0] +
                                (EARTH_RADIUS + altitude) / UNIT_LENGTH,
                                e_spherical[1],
                                e_spherical[2]]) 
        c_cartesian = get_position_cartesian_from_spherical(c_spherical[0], c_spherical[1], c_spherical[2]);

        cv_leo_cartesian = np.cross(e_orbital_plane_cartesian, c_cartesian)
        cv_leo_cartesian_unit = cv_leo_cartesian / np.linalg.norm(cv_leo_cartesian)
        
        e_speed = UNIT_VELOCITY * get_speed_cartesian(ev_cartesian[0], ev_cartesian[1], ev_cartesian[2])
        leo_speed = get_circular_orbit_speed("Earth", altitude)
        cv_cartesian = (ev_cartesian_unit * e_speed +
                        cv_leo_cartesian_unit * leo_speed) / UNIT_VELOCITY
        c_speed = UNIT_VELOCITY * get_speed_cartesian(cv_cartesian[0], cv_cartesian[1], cv_cartesian[2])
        cv_spherical = np.array(get_velocity_spherical_from_cartesian(c_cartesian, cv_cartesian))

        """
        e_s_distance = get_distance_spherical(e_spherical, s_spherical) * UNIT_LENGTH
        c_e_distance = get_distance_spherical(c_spherical, e_spherical) * UNIT_LENGTH
        c_m_distance = get_distance_spherical(c_spherical, m_spherical) * UNIT_LENGTH
        """
        print("===========================", n, i, j, k, days[i], "===============================")
        print("e_orbital_plane_cartesian=", e_orbital_plane_cartesian)
        print("e_cartesian=", e_cartesian)
        print("c_cartesian=", c_cartesian)
#        print("e_s_distance=", e_s_distance)
        print("c_e_distance=", c_e_distance)
#        print("c_m_distance=", c_m_distance)
        print("----------------------------------------------------")
        print("tilt=", tilts[k])
        print("ev_cartesian=", ev_cartesian)
        print("cv_cartesian=", cv_cartesian)
        #print("burn_cartesian=", burn_cartesian)
        print("ev_cartesian_unit=", ev_cartesian_unit)
        print("c_leo_cartesian_unit=", c_leo_cartesian_unit)
        print("leo_cartesian_unit=", leo_cartesian_unit)
        print("burn_cartesian_unit=", burn_cartesian_unit)
        print("----------------------------------------------------")
        print("e_speed=", e_speed)
        print("leo_speed=", leo_speed)
        print("burn_speed=", burn_speed)
        print("c_speed=", c_speed)
        print("----------------------------------------------------")
        print("e_spherical=", e_spherical)
        print("c_spherical=", c_spherical)
        print("ev_spherical=", ev_spherical)
        print("cv_spherical=", cv_spherical)
        print("====================================================")
        """
        # FINAL OUTPUT: Initial coordinates (Q)
        Q0s[n] = c_spherical

        # FINAL OUTPUT: Initial momenta per mass (B)
        R, theta, _ = c_spherical
        Rdot, thetadot, phidot = cv_spherical

        B_R = get_B_R(Rdot)
        B_theta = get_B_theta(R, thetadot)
        B_phi = get_B_phi(R, theta, phidot)

        B0s[n] = np.array([B_R, B_theta, B_phi])

    return day0s, Q0s, B0s

def get_leo_positions_and_velocities_C(days=[0], burndvs=[0], tilts=[0], h = 0.1 / UNIT_TIME, altitude=160, max_year="2020"):
    days = np.asarray(days)
    burndvs = np.asarray(burndvs)
    tilts = np.asarray(tilts)

    day0s = np.zeros((len(days) * len(burndvs) * len(tilts)))
    Q0s = np.zeros((len(days) * len(burndvs) * len(tilts), 3))
    B0s = np.zeros((len(days) * len(burndvs) * len(tilts), 3))

    ephemerides = get_ephemerides(max_year=max_year)
    earth = np.array(ephemerides['earth'])
    mars = np.array(ephemerides['mars'])
    earth_R = earth[:,3].astype(np.float64)
    earth_theta = earth[:,4].astype(np.float64) * pi / 180
    earth_phi = earth[:,5].astype(np.float64) * pi / 180
    mars_R = mars[:,3].astype(np.float64)
    mars_theta = mars[:,4].astype(np.float64) * pi / 180
    mars_phi = mars[:,5].astype(np.float64) * pi / 180

    cudasim.initial_conditions.restype = None
    cudasim.initial_conditions.argtypes = [
        c_int,
        POINTER(c_double),
        c_int,
        POINTER(c_double),
        c_int,
        POINTER(c_double),
        c_double,
        c_int,
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
    ]

    days_ctype = days.ctypes.data_as(POINTER(c_double))
    burndvs_ctype = burndvs.ctypes.data_as(POINTER(c_double))
    tilts_ctype = tilts.ctypes.data_as(POINTER(c_double))
    day0s_ctype = day0s.ctypes.data_as(POINTER(c_double))
    Q0s_ctype = Q0s.ctypes.data_as(POINTER(c_double))
    B0s_ctype = B0s.ctypes.data_as(POINTER(c_double))
    earth_R_ctype = earth_R.ctypes.data_as(POINTER(c_double))
    earth_theta_ctype = earth_theta.ctypes.data_as(POINTER(c_double))
    earth_phi_ctype = earth_phi.ctypes.data_as(POINTER(c_double))
    mars_R_ctype = mars_R.ctypes.data_as(POINTER(c_double))
    mars_theta_ctype = mars_theta.ctypes.data_as(POINTER(c_double))
    mars_phi_ctype = mars_phi.ctypes.data_as(POINTER(c_double))

    cudasim.initial_conditions(
        int(days.size),
        days_ctype,
        int(burndvs.size),
        burndvs_ctype,
        int(tilts.size),
        tilts_ctype,
        altitude,
        int(earth_R.size),
        earth_R_ctype,
        earth_theta_ctype,
        earth_phi_ctype,
        mars_R_ctype,
        mars_theta_ctype,
        mars_phi_ctype,
        day0s_ctype,
        Q0s_ctype,
        B0s_ctype,
    )
    return day0s, Q0s, B0s
