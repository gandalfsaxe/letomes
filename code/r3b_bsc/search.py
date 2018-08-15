"""
Brute-force search Module for reduced 3-body solver
===================================================

Functions:

We assume **TODO FILL OUT HERE!

"""

from __future__ import print_function

import sys
import time
from math import ceil
from multiprocessing import Pool

import numpy as np

from orbsim import DAY
from orbsim.r3b_2d import (
    EARTH_POSITION_X,
    LEO_RADIUS_NONDIM,
    LEO_VELOCITY,
    UNIT_TIME,
    UNIT_VELOCITY,
)

from .symplectic import symplectic


def print_search_results(stat, pos, ang, burn, x0, y0, p0_x, p0_y, dv, toa):
    print(
        "# --------------------------------------------------------------------------"
    )
    print("duration = %i/unit_time" % (max(1, int(ceil(toa * UNIT_TIME)))))
    print("pos      = %.15lf" % (pos))
    print("ang      = %.15lf" % (ang))
    print("burn     = %.15lf/unit_velocity" % (burn * UNIT_VELOCITY))
    print("x0       = %.15lf" % (x0))
    print("y0       = %.15lf" % (y0))
    print("p0_x      = %.15lf" % (p0_x))
    print("p0_y      = %.15lf" % (p0_y))
    print(
        "# --------------------------------------------------------------------------"
    )
    print("# dV(earth-escape) = %f km/s" % (abs(burn) * UNIT_VELOCITY))
    if stat > 0 and stat < 100:
        print("# Min moon distance= %f" % (stat))
    elif stat < 0:
        print("# dV(moon-capture) = %f km/s" % (dv * UNIT_VELOCITY))
        print("# dV(total)        = %f km/s" % ((abs(burn) + dv) * UNIT_VELOCITY))
        print("# Flight-time      = %f days" % (toa * UNIT_TIME))
    else:
        print("# Crashed on earth!")
    print(
        "# --------------------------------------------------------------------------"
    )
    sys.stdout.flush()


def search(thread, threads, n, duration, positions, angles, burns):

    # print("Start thread=%i" % (thread))

    # Initialize arrays
    xs = np.zeros(n)
    ys = np.zeros(n)
    p_xs = np.zeros(n)
    p_ys = np.zeros(n)
    step_errors = np.zeros(n)
    h_list = np.zeros(n)
    info = np.zeros(2)

    # Search for orbits
    trials = len(positions) * len(angles) * len(burns)
    ld1 = len(angles) * len(burns)
    ld2 = len(burns)
    trial = 0
    hit_earth = 0
    hit_moon = 0
    best_status = 1e9
    progress = -1
    i = thread
    while i < trials:

        # One-to-one mapping of i -> (pos_i,ang_i,burn_i)
        pos_i = i // ld1
        ang_i = (i - pos_i * ld1) // ld2
        burn_i = i - pos_i * ld1 - ang_i * ld2
        i += threads

        # Find launch setup
        pos = positions[pos_i]
        ang = angles[ang_i]
        burn = burns[burn_i]

        # Calculate initial conditions
        x0 = np.cos(pos) * LEO_RADIUS_NONDIM
        y0 = np.sin(pos) * LEO_RADIUS_NONDIM
        v_norm_x = -y0 / LEO_RADIUS_NONDIM
        v_y_norm = x0 / LEO_RADIUS_NONDIM
        v_x = (LEO_VELOCITY / UNIT_VELOCITY) * v_norm_x
        v_y = (LEO_VELOCITY / UNIT_VELOCITY) * v_y_norm
        x0 += EARTH_POSITION_X
        bx = np.cos(ang) * v_norm_x - np.sin(ang) * v_y_norm
        by = np.sin(ang) * v_norm_x + np.cos(ang) * v_y_norm
        p0_x = (
            v_x + burn * bx - y0
        )  # Sign of burn decides rotational direction of launch
        p0_y = v_y + burn * by + x0

        # Call symplectic integration
        # status > 0     : Closest distance to moon achieved
        # status < 0     : Hit the moon using status=dV(moon)-10000 to get into orbit
        # status == 100  : Collided with earth
        # if thread == 1:
        #    print(n,duration,x0,y0,p0_x,p0_y)
        status = symplectic(
            n,
            duration,
            x0,
            y0,
            p0_x,
            p0_y,
            xs,
            ys,
            p_xs,
            p_ys,
            step_errors,
            h_list,
            info,
        )
        if status == 100:
            hit_earth += 1
        if status < 0:
            hit_moon += 1
        if status < best_status:
            best_status = status
            best_pos = pos
            best_ang = ang
            best_burn = burn
            best_x0 = x0
            best_y0 = y0
            best_p0_x = p0_x
            best_p0_y = p0_y
            best_dv = info[0]
            best_toa = info[1]

        # Show progress
        if thread == 0:  # only thread 0
            if (100 * trial / (1 + trials // threads)) // 10 > progress:
                progress = (100 * trial / (1 + trials // threads)) // 10
                print(progress * 10, end="% ")
                sys.stdout.flush()
            trial += 1
        # if thread == 13:
        #   print("thread=%i status=%f best_status=%f trial=%i(%i) pos=%f ang=%f burn=%f" % (thread,status,best_status,trial,trials,pos,ang,burn))

    # print("End thread=%i" % (thread))

    return (
        best_status,
        best_pos,
        best_ang,
        best_burn,
        best_x0,
        best_y0,
        best_p0_x,
        best_p0_y,
        best_dv,
        best_toa,
        hit_earth,
        hit_moon,
    )


def search_worker(args):
    return search(args[0], args[1], args[2], args[3], args[4], args[5], args[6])


def search_mt(
    threads,
    n,
    duration,
    num_pos,
    num_ang,
    num_burn,
    pos_low,
    pos_high,
    ang_low,
    ang_high,
    burn_low,
    burn_high,
):

    # Time search
    runtime = time.time()

    # Set search space
    positions = np.linspace(pos_low, pos_high, num_pos)
    angles = np.linspace(ang_low, ang_high, num_ang)
    burns = np.linspace(burn_low, burn_high, num_burn)
    if num_pos == 1:
        positions[0] = (pos_high + pos_low) / 2.0
    if num_ang == 1:
        angles[0] = (ang_high + ang_low) / 2.0
    if num_burn == 1:
        burns[0] = (burn_high + burn_low) / 2.0
    if num_burn == 2:
        burns[0] = burn_low
        burns[1] = burn_high
    trials = num_pos * num_ang * num_burn
    print(positions)
    print(angles)
    print(burns * UNIT_VELOCITY)

    # Set threads
    threads = min(threads, num_pos)

    # Do multi-threaded search
    print(
        "# --------------------------------------------------------------------------"
    )
    print("# Threads:          %6i" % (threads))
    print("# Trials:           %6i (" % (trials), end="")
    if threads == 1:
        # Single thread
        best_status, best_pos, best_ang, best_burn, best_x0, best_y0, best_p0_x, best_p0_y, best_dv, best_toa, hit_earth, hit_moon = search(
            0, num_pos, n, duration, positions, angles, burns
        )
    else:
        # Multi-threading
        chunk = num_pos / threads
        args = [
            [i, threads, n, duration, positions, angles, burns] for i in range(threads)
        ]
        pool = Pool()
        result = pool.map(search_worker, args)
        pool.close()
        pool.join()

        # Reduce results from all threads
        best_status = 1e9
        hit_earth = 0
        hit_moon = 0
        for i in range(threads):
            status = result[i][0]
            if status < best_status:
                best_status = status
                best_pos = result[i][1]
                best_ang = result[i][2]
                best_burn = result[i][3]
                best_x0 = result[i][4]
                best_y0 = result[i][5]
                best_p0_x = result[i][6]
                best_p0_y = result[i][7]
                best_dv = result[i][8]
                best_toa = result[i][9]
                hit_earth += result[i][10]
                hit_moon += result[i][11]

    print("100%)")
    print(
        "# No interception:  %6i (%i%%)"
        % (
            trials - hit_earth - hit_moon,
            100 * (trials - hit_earth - hit_moon) / trials,
        )
    )
    print("# Crashed on earth: %6i (%i%%)" % (hit_earth, 100 * hit_earth / trials))
    print("# Hit moon:         %6i (%i%%)" % (hit_moon, 100 * hit_moon / trials))
    runtime = time.time() - runtime
    print("# Runtime:          %6.2fs" % (runtime))
    if best_status < 100:
        print_search_results(
            best_status,
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
        return (
            best_status,
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
    else:
        return best_status, 0, 0, 0, 0, 0, 0, 0, 0, 0
