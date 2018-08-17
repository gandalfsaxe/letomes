"""
Reduced 3-Body Problem Solver Module
====================================
A collection of various numerical solvers for the reduced 3-body problem consisting of two larger masses (Earth, Moon) and one smaller moving in their gravitational field (a satellite). The solution assumes Earth-Moon center of mass as origin and a cartesian x-y coordinate system rotating with the lines connecting the Earth and Moon (non-inertial frame accounted for in the equations of motion).

Functions:

We assume **TODO FILL OUT HERE!

"""

import time
from math import pi, sqrt

import numpy as np

from orbsim import DAY
from orbsim.r3b_2d import (
    LLO_RADIUS,
    LLO_VELOCITY,
    UNIT_LENGTH,
    UNIT_TIME,
    UNIT_VELOCITY,
)

from .search import print_search_results, search, search_mt
from .symplectic import symplectic

# from orbsim.constants import *


# ** pos, ang, burn are not used for anything beside printing
def trajectory(n, duration, pos, ang, burn, x0, y0, p0_x, p0_y):
    """Integrate trajectory for the reduced 3-body problem.

    Args:
        n (int): Positions stored.
        duration (float): Time duration of simulation.
        x0 (float): Initial x-coordinate
        y0 (float): Initial y-coordinate
        p0_x (float): Initial generalized x-momentum
        p0_y (float): Initial generalized y-momentum

    Returns:
        Tuple of time-, x-, y-, p_x- and p_y lists.
    
    """
    print("# Running trajectory.")

    # Initialize arrays
    ts = np.linspace(0, duration, n)
    xs = np.zeros(n)
    ys = np.zeros(n)
    p_xs = np.zeros(n)
    p_ys = np.zeros(n)
    step_errors = np.zeros(n)
    h_list = np.zeros(n)
    info = np.zeros(2)

    # Find orbits
    runtime = time.time()
    status = symplectic(
        n, duration, x0, y0, p0_x, p0_y, xs, ys, p_xs, p_ys, step_errors, h_list, info
    )
    runtime = time.time() - runtime

    # Display result
    print_search_results(status, pos, ang, burn, x0, y0, p0_x, p0_y, info[0], info[1])
    print("# Runtime = %3.2fs" % (runtime))
    return ts, xs, ys, p_xs, p_ys, step_errors, h_list


def hohmann(threads, n):
    """Finding Hohmann trajectory for the reduced 3-body problem.

    Args:
        n (int): Positions stored.

    Returns:
        Tuple of time-, x-, y-, p_x- and p_y lists.
    
    """

    print("# Running Hohmann.")

    # Hohmann trajectory < 6 days
    duration = 6 / UNIT_TIME
    best_total_dv = 1e9
    positions = 100
    angles = 1
    burns = 200
    pos = -3 * pi / 4
    ang = 0
    burn = 3.11 / UNIT_VELOCITY  # Forward Hohmann
    # burn_low = -3.14/unit_velocity # Reverse Hohmann

    # Super fast Hohmann trajectory < 1 days
    # duration = 3/unit_time
    # best_total_dv = 1e9
    # positions = 10
    # angles = 10
    # burns = 200
    # pos = -3*pi/4
    # ang = 0
    # burn = 3.7/unit_velocity # Forward Hohmann

    pos_range = pi / 4
    ang_range = pi / 8
    burn_range = 0.1 / UNIT_VELOCITY

    # Start search
    searches = 0
    max_searches = 5
    while searches < max_searches:
        runtime = time.time()
        searches += 1
        print("############## Search %i ###############" % (searches))
        print("# pos              = %f" % (pos))
        print("# ang              = %f" % (ang))
        print("# burn             = %f" % (burn))
        pos_low = pos - pos_range
        pos_high = pos + pos_range
        ang_low = ang - ang_range
        ang_high = ang + ang_range
        burn_low = burn - burn_range
        burn_high = burn + burn_range
        stat, pos, ang, burn, x0, y0, p0_x, p0_y, dv, toa = search_mt(
            threads,
            1,
            duration,
            positions,
            angles,
            burns,
            pos_low,
            pos_high,
            ang_low,
            ang_high,
            burn_low,
            burn_high,
        )

        if stat < 0:
            total_dv = abs(burn) + dv
            if best_total_dv > total_dv:
                best_total_dv = total_dv
                best_stat = stat
                best_pos = pos
                best_ang = ang
                best_burn = burn
                best_x0 = x0
                best_y0 = y0
                best_p0_x = p0_x
                best_p0_y = p0_y
                best_dv = dv
                best_toa = toa
            else:
                break

        pos_range *= 0.1
        ang_range *= 0.1
        burn_range *= 0.1

        runtime = time.time() - runtime
        print("# Search runtime   = %3.2fs" % (runtime))

    # Print best result
    print("################ Best ################")
    print("# Best dV(total)   = %f km/s" % (best_total_dv * UNIT_VELOCITY))
    print_search_results(
        best_stat,
        best_pos,
        best_ang,
        best_burn,
        best_x0,
        best_y0,
        best_p0_x,
        best_p0_y,
        best_dv,
        best_toa,
    )

    # Initialize arrays
    ts = np.linspace(0, duration, n)
    xs = np.zeros(n)
    ys = np.zeros(n)
    p_xs = np.zeros(n)
    p_ys = np.zeros(n)
    step_errors = np.zeros(n)
    h_list = np.zeros(n)
    info = np.zeros(2)

    # Do trajectory
    duration = 10 / UNIT_TIME
    status = symplectic(
        n, duration, x0, y0, p0_x, p0_y, xs, ys, p_xs, p_ys, step_errors, h_list, info
    )

    return ts, xs, ys, p_xs, p_ys, step_errors, h_list


def low_energy(threads, n):
    """Finding low energy transfer trajectory for the reduced 3-body problem.

    Args:
        n (int): Positions stored.

    Returns:
        Tuple of time-, x-, y-, p_x- and p_y lists.
    
    """

    print("# Running low_energy.")

    # Low-energy trajectory < 200 days
    duration = 200 / UNIT_TIME
    best_total_dv = 1e9
    positions = 100
    angles = 1
    burns = 200
    pos = -3 * pi / 4
    ang = 0
    burn = 3.12 / UNIT_VELOCITY
    pos_range = pi
    ang_range = 0
    burn_range = 0.01 / UNIT_VELOCITY

    # Start search
    searches = 0
    max_searches = 1
    while searches < max_searches:
        runtime = time.time()
        searches += 1
        print("############## Search %i ###############" % (searches))
        print("# pos              = %f" % (pos))
        print("# ang              = %f" % (ang))
        print("# burn             = %f" % (burn))
        pos_low = pos - pos_range
        pos_high = pos + pos_range
        ang_low = ang - ang_range
        ang_high = ang + ang_range
        burn_low = burn - burn_range
        burn_high = burn + burn_range
        stat, pos, ang, burn, x0, y0, p0_x, p0_y, dv, toa = search_mt(
            threads,
            1,
            duration,
            positions,
            angles,
            burns,
            pos_low,
            pos_high,
            ang_low,
            ang_high,
            burn_low,
            burn_high,
        )

        if stat < 0:
            total_dv = abs(burn) + dv
            if best_total_dv > total_dv:
                best_total_dv = total_dv
                best_stat = stat
                best_pos = pos
                best_ang = ang
                best_burn = burn
                best_x0 = x0
                best_y0 = y0
                best_p0_x = p0_x
                best_p0_y = p0_y
                best_dv = dv
                best_toa = toa
            else:
                break

        pos_range *= 0.1
        ang_range *= 0.1
        burn_range *= 0.1

        runtime = time.time() - runtime
        print("# Search runtime   = %3.2fs" % (runtime))

    # Initialize arrays
    ts = np.linspace(0, duration, n)
    xs = np.zeros(n)
    ys = np.zeros(n)
    p_xs = np.zeros(n)
    p_ys = np.zeros(n)
    step_errors = np.zeros(n)
    h_list = np.zeros(n)
    info = np.zeros(2)

    # Do trajectory
    duration = toa + (2.0 * pi * LLO_RADIUS / LLO_VELOCITY) / (UNIT_TIME * DAY)
    status = symplectic(
        n, duration, x0, y0, p0_x, p0_y, xs, ys, p_xs, p_ys, step_errors, h_list, info
    )
    exit()
    return ts, xs, ys, p_xs, p_ys, step_errors, h_list


def low_energy_parts8(threads, n):
    """Finding low energy transfer trajectory for the reduced 3-body problem.

    Args:
        n (int): Positions stored.

    Returns:
        Tuple of time-, x-, y-, p_x- and p_y lists.
    
    """

    print("# Running low_energy_parts8.")

    # Low-energy-short trajectory < 47 days
    duration = 200 / UNIT_TIME
    best_total_dv = 1e9
    best_toa = 0
    positions = 55
    angles = 1
    burns = 55

    # Divide circular earth orbit into 8 parts
    for i in range(0, 8):
        pos = i * pi / 4
        ang = 0
        # burn = 3.12/unit_velocity # moon
        burn = 3.09 / UNIT_VELOCITY  # L1
        pos_range = 2 * pi / 16
        ang_range = pi / 2
        burn_range = 0.1 / UNIT_VELOCITY

        # Start search
        searches = 0
        max_searches = 3
        while searches < max_searches:
            runtime = time.time()
            searches += 1
            print("############## Search %i ###############" % (searches))
            print("# pos              = %f" % (pos))
            print("# ang              = %f" % (ang))
            print("# burn             = %f" % (burn))
            pos_low = pos - pos_range
            pos_high = pos + pos_range
            ang_low = ang - ang_range
            ang_high = ang + ang_range
            burn_low = burn - burn_range
            burn_high = burn + burn_range
            stat, pos, ang, burn, x0, y0, p0_x, p0_y, dv, toa = search_mt(
                threads,
                1,
                duration,
                positions,
                angles,
                burns,
                pos_low,
                pos_high,
                ang_low,
                ang_high,
                burn_low,
                burn_high,
            )

            if stat < 0:
                total_dv = abs(burn) + dv
                if best_total_dv > total_dv:
                    best_total_dv = total_dv
                    best_stat = stat
                    best_pos = pos
                    best_ang = ang
                    best_burn = burn
                    best_x0 = x0
                    best_y0 = y0
                    best_p0_x = p0_x
                    best_p0_y = p0_y
                    best_dv = dv
                    best_toa = toa
                else:
                    break

            pos_range *= 0.1
            ang_range *= 0.1
            burn_range *= 0.1

            runtime = time.time() - runtime
            print("# Search runtime   = %3.2fs" % (runtime))

    # Print best result
    if best_total_dv < 1e9:
        print("################ Best ################")
        print("# Best dV(total)   = %f km/s" % (best_total_dv * UNIT_VELOCITY))
        print_search_results(
            best_stat,
            best_pos,
            best_ang,
            best_burn,
            best_x0,
            best_y0,
            best_p0_x,
            best_p0_y,
            best_dv,
            best_toa,
        )

    # Initialize arrays
    ts = np.linspace(0, duration, n)
    xs = np.zeros(n)
    ys = np.zeros(n)
    p_xs = np.zeros(n)
    p_ys = np.zeros(n)
    step_errors = np.zeros(n)
    h_list = np.zeros(n)
    info = np.zeros(2)

    # Do trajectory
    # duration = toa+(2.0*pi*llo_radius/llo_velocity)/(unit_time*day)
    status = symplectic(
        n, duration, x0, y0, p0_x, p0_y, xs, ys, p_xs, p_ys, step_errors, h_list, info
    )
    # exit()
    return ts, xs, ys, p_xs, p_ys, step_errors, h_list


def refine(threads, n, duration, pos, ang, burn, x0, y0, p0_x, p0_y):
    """Integrate trajectory for the reduced 3-body problem.

    Args:
        n (int): Positions stored.
        duration (float): Time duration of simulation.
        x0 (float): Initial x-coordinate
        y0 (float): Initial y-coordinate
        p0_x (float): Initial generalized x-momentum
        p0_y (float): Initial generalized y-momentum

    Returns:
        Tuple of time-, x-, y-, p_x- and p_y lists.
    
    """
    print("# Running refine.")

    # Low-energy-long trajectory < 200 days
    # duration = 200/unit_time
    # Low-energy-short trajectory < 47 days
    # duration = 47/unit_time
    best_total_dv = 1e9
    best_toa = 0
    positions = 15
    angles = 15
    burns = 15

    # Divide circular earth orbit into 8 parts
    pos_range = 2 * pi / 16 * 0.1
    ang_range = pi / 100 * 0.1
    burn_range = 0.1 / UNIT_VELOCITY * 0.1

    # Start search
    searches = 0
    max_searches = 10
    while searches < max_searches:
        runtime = time.time()
        searches += 1
        print("############## Search %i ###############" % (searches))
        print("# pos              = %f" % (pos))
        print("# ang              = %f" % (ang))
        print("# burn             = %f" % (burn))
        pos_low = pos - pos_range
        pos_high = pos + pos_range
        ang_low = ang - ang_range
        ang_high = ang + ang_range
        burn_low = burn - burn_range
        burn_high = burn + burn_range
        stat, pos, ang, burn, x0, y0, p0_x, p0_y, dv, toa = search_mt(
            threads,
            1,
            duration,
            positions,
            angles,
            burns,
            pos_low,
            pos_high,
            ang_low,
            ang_high,
            burn_low,
            burn_high,
        )

        if stat < 0:
            total_dv = abs(burn) + dv
            if best_total_dv > total_dv:
                best_total_dv = total_dv
                best_stat = stat
                best_pos = pos
                best_ang = ang
                best_burn = burn
                best_x0 = x0
                best_y0 = y0
                best_p0_x = p0_x
                best_p0_y = p0_y
                best_dv = dv
                best_toa = toa
            else:
                break

        pos_range *= 0.1
        ang_range *= 0.1
        burn_range *= 0.1

        runtime = time.time() - runtime
        print("# Search runtime   = %3.2fs" % (runtime))

    # Print best result
    print("################ Best ################")
    print("# Best dV(total)   = %f km/s" % (best_total_dv * UNIT_VELOCITY))
    print_search_results(
        best_stat,
        best_pos,
        best_ang,
        best_burn,
        best_x0,
        best_y0,
        best_p0_x,
        best_p0_y,
        best_dv,
        best_toa,
    )

    # Initialize arrays
    ts = np.linspace(0, duration, n)
    xs = np.zeros(n)
    ys = np.zeros(n)
    p_xs = np.zeros(n)
    p_ys = np.zeros(n)
    step_errors = np.zeros(n)
    h_list = np.zeros(n)
    info = np.zeros(2)

    # Do trajectory
    duration = toa + (2.0 * pi * LLO_RADIUS / LLO_VELOCITY) / (UNIT_TIME * DAY)
    status = symplectic(
        n, duration, x0, y0, p0_x, p0_y, xs, ys, p_xs, p_ys, step_errors, h_list, info
    )
    # exit()
    return ts, xs, ys, p_xs, p_ys, step_errors, h_list