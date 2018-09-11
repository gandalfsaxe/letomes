"""
Reduced 3-body Problem testing script
====================================
Testing the reduced 3-body problem solvers with different numerical algorithms.
TODO: Add more description + how to use
"""
import multiprocessing
import os
import pathlib
import sys
import time
from math import cos, pi, sin

import matplotlib.pyplot as plt
import numpy as np

from orbsim import DAY, EARTH_RADIUS, LUNAR_RADIUS
from orbsim.r3b_2d import (
    EARTH_POSITION_X,
    L1_POSITION_X,
    LEO_RADIUS,
    LEO_VELOCITY,
    LLO_RADIUS,
    LLO_VELOCITY,
    LUNAR_POSITION_X,
    ORBITAL_TOLERANCE,
    UNIT_LENGTH,
    UNIT_TIME,
    UNIT_VELOCITY,
    k,
)
from r3b_bsc import reduced3body as r3b


def run_test():

    MODE = sys.argv[1]

    FORMAT = "png"
    # FORMAT = "pdf"

    mode_dict = {
        # Keys: Possible input arguments (argv)
        # Values: Output folder name of associated log/figs of run
        # Precalculated initial conditions for specific orbit types
        "leo": "demo_leo_closed",
        "llo": "demo_llo_closed",
        "h": "demo_hohmann",
        "h3": "demo_hohmann_3_days",
        "h1": "demo_hohmann_1_day",
        "hr": "demo_hohmann_reverse",
        "ls": "demo_leto_short",
        "ll": "demo_leto_long",
        # "l1": "demo_L1",  # TODO: Takes a long time, probably doesn't work, look at later
        # Search for trajectories
        "sh": "search_hohmann",
        "sl": "search_leto",  # FIXME: Figure out why no figs when search_hohmann have
        # "slp8": "search_low_energy_parts_8",  # TODO: Doesn't work - what does it do?
        # "sr": "search_refine"  # TODO: Doesn't work - what does it do?
    }
    MODE_NAME = mode_dict[MODE]

    OUTPUT_DIR = "tests/" + MODE_NAME + "/"

    pathlib.Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    # All prints are redirected to log file
    old_stdout = sys.stdout
    log_file = open(OUTPUT_DIR + "log_" + MODE_NAME + ".log", "w")
    sys.stdout = log_file

    # Threads will typically be 8 on quadcore machines
    threads = multiprocessing.cpu_count()  # If raises NotImplementedError, do this instead https://stackoverflow.com/a/14840102/2948823 

    runtime = time.time()

    n = 1000000  # FIXME: What the duck is n doing here

    # Set coordinates
    if MODE == "leo":  # Low Earth Orbit, one closed orbit
        duration = (2.0 * pi * LEO_RADIUS / LEO_VELOCITY) / (UNIT_TIME * DAY)
        r = LEO_RADIUS / UNIT_LENGTH
        v = 0.99732 * LEO_VELOCITY / UNIT_VELOCITY
        theta = 0
        x = r * cos(theta)
        y = r * sin(theta)
        v_x = -v * y / r
        v_y = v * x / r
        pos = 0
        ang = 0
        burn = 0
        x0 = EARTH_POSITION_X + x
        y0 = y
        p0_x = v_x - y0
        p0_y = v_y + x0
    elif MODE == "llo":  # Low Lunar Orbit, one closed orbit
        duration = (2.0 * pi * LLO_RADIUS / LLO_VELOCITY) / (UNIT_TIME * DAY)
        r = LLO_RADIUS / UNIT_LENGTH
        v = 0.99732 * LLO_VELOCITY / UNIT_VELOCITY
        theta = 0
        x = r * cos(theta)
        y = r * sin(theta)
        v_x = -v * y / r
        v_y = v * x / r
        pos = 0
        ang = 0
        burn = 0
        x0 = LUNAR_POSITION_X + x
        y0 = y
        p0_x = v_x - y0
        p0_y = v_y + x0
    elif MODE == "h":  # Hohmann transfer orbit
        # MODE = 'search_refine'
        # --------------------------------------------------------------------------
        duration = 5 / UNIT_TIME
        pos = -2.086814820119193
        ang = -0.000122173047640
        burn = 3.111181716545691 / UNIT_VELOCITY
        x0 = -0.020532317163607
        y0 = -0.014769797663479
        p0_x = 9.302400979050308
        p0_y = -5.289712560652044
        # --------------------------------------------------------------------------
        # dV(earth-escape) = 3.111182 km/s
        # dV(moon-capture) = 0.800682 km/s
        # dV(total)        = 3.911863 km/s
        # Flight-time      = 4.300078 days
        # --------------------------------------------------------------------------
    elif MODE == "hr":  # Reverse Hohmann
        # --------------------------------------------------------------------------
        duration = 4 / UNIT_TIME
        pos = -2.282942228154665
        ang = 0.000000000000000
        burn = -3.149483130653266 / UNIT_VELOCITY
        x0 = -0.023249912090507
        y0 = -0.012853859046429
        p0_x = -8.098481905534163
        p0_y = 6.978997254692934
        # --------------------------------------------------------------------------
        # dV(earth-escape) = 3.149483 km/s
        # dV(moon-capture) = 0.968488 km/s
        # dV(total)        = 4.117971 km/s
        # Flight-time      = 3.875497 days
        # --------------------------------------------------------------------------
    elif MODE == "ll":  # LETO long
        # --------------------------------------------------------------------------
        duration = 195 / UNIT_TIME
        pos = 3.794182930145708
        ang = 0.023901745288554
        burn = 3.090702702702703 / UNIT_VELOCITY
        x0 = -0.025645129237870
        y0 = -0.010311570301966
        p0_x = 6.539303578815582
        p0_y = -8.449205705334165
        # --------------------------------------------------------------------------
        # dV(earth-escape) = 3.090703 km/s
        # dV(moon-capture) = 0.704114 km/s
        # dV(total)        = 3.794816 km/s
        # Flight-time      = 194.275480 days
        # --------------------------------------------------------------------------
        # --------------------------------------------------------------------------
        # MODE = 'search_refine'
        #    duration = 195/unit_time
        #    pos      = 3.794182930145708
        #    ang      = 0.023901745288554
        #    burn     = 3.090702702702703/unit_velocity
        #    x0       = -0.025645129237870
        #    y0       = -0.010311570301966
        #    p0_x      = 6.539303578815583
        #    p0_y      = -8.449205705334164
        # --------------------------------------------------------------------------
        # dV(earth-escape) = 3.090703 km/s
        # dV(moon-capture) = 0.704114 km/s
        # dV(total)        = 3.794817 km/s
        # Flight-time      = 194.275480 days
        # --------------------------------------------------------------------------
    elif MODE == "ls":  # LETO short
        # MODE = 'search_refine'
        # --------------------------------------------------------------------------
        duration = 41 / UNIT_TIME
        pos = -0.138042744751570
        ang = -0.144259374836607
        burn = 3.127288444444444 / UNIT_VELOCITY
        x0 = 0.004665728429046
        y0 = -0.002336647636098
        p0_x = 1.904735175752430
        p0_y = 10.504985512873279
        # --------------------------------------------------------------------------
        # dV(earth-escape) = 3.127288 km/s
        # dV(moon-capture) = 0.768534 km/s
        # dV(total)        = 3.895822 km/s
        # Flight-time      = 40.617871 days
        # --------------------------------------------------------------------------
    elif MODE == "h3":  # 3-day Hohmann
        # MODE = 'search_refine'
        # --------------------------------------------------------------------------
        duration = 3 / UNIT_TIME
        pos = -2.272183066647597
        ang = -0.075821466029764
        burn = 3.135519748743719 / UNIT_VELOCITY
        x0 = -0.023110975767437
        y0 = -0.012972499765730
        p0_x = 8.032228991913522
        p0_y = -7.100537706154897
        # --------------------------------------------------------------------------
        # dV(earth-escape) = 3.135520 km/s
        # dV(moon-capture) = 0.879826 km/s
        # dV(total)        = 4.015346 km/s
        # Flight-time      = 2.999939 days
        # --------------------------------------------------------------------------
    elif MODE == "h1":  # 1-day Hohmann
        # MODE = 'search_refine'
        duration = 1 / UNIT_TIME
        pos = -2.277654673852600
        ang = 0.047996554429844
        burn = 3.810000000000000 / UNIT_VELOCITY
        x0 = -0.023181791813268
        y0 = -0.012912351430812
        p0_x = 8.764829132987316
        p0_y = -7.263069305305378
        # --------------------------------------------------------------------------
        # dV(earth-escape) = 3.810000 km/s
        # dV(moon-capture) = 3.319455 km/s
        # dV(total)        = 7.129455 km/s
        # Flight-time      = 0.997234 days
        # --------------------------------------------------------------------------
    elif MODE == "l1":  # Earth to L1 point
        MODE = "search_refine"
        # --------------------------------------------------------------------------
        duration = 191 / UNIT_TIME
        pos = 2.843432239707429
        ang = 0.000000000000000
        burn = 3.091851851851852 / UNIT_VELOCITY
        x0 = -0.028385246222264
        y0 = 0.004988337832881
        p0_x = -3.136296304910217
        p0_y = -10.217405925499762
        # --------------------------------------------------------------------------
        # dV(earth-escape) = 3.091852 km/s
        # dV(at L1)        = 0.676226 km/s
        # dV(total)        = 3.768078 km/s
        # Flight-time      = 190.001881 days
        # --------------------------------------------------------------------------

    #################### FUNCTION CALLS ####################

    if MODE == "sh":  # Search for Hohmann:
        ts, xs, ys, p_xs, p_ys, step_errors, h_list = r3b.hohmann(threads, n)
    elif MODE == "sl":  # Search for LETO
        ts, xs, ys, p_xs, p_ys, step_errors, h_list = r3b.low_energy(threads, n)
    elif MODE == "sl_parts8":
        ts, xs, ys, p_xs, p_ys, step_errors, h_list = r3b.low_energy_parts8(threads, n)
    elif MODE == "search_refine":
        ts, xs, ys, p_xs, p_ys, step_errors, h_list = r3b.refine(
            threads, n, duration, pos, ang, burn, x0, y0, p0_x, p0_y
        )
    else:
        ts, xs, ys, p_xs, p_ys, step_errors, h_list = r3b.trajectory(
            n, duration, pos, ang, burn, x0, y0, p0_x, p0_y
        )
    H_list = (
        p_xs ** 2 / 2
        + p_ys ** 2 / 2
        + ys * p_xs
        - xs * p_ys
        - (1 - k) / np.sqrt(np.power(k + xs, 2) + np.power(ys, 2))
        - k / np.sqrt(np.power(1 - k - xs, 2) + np.power(ys, 2))
    )
    print("# Final position: %f %f" % (xs[n - 1], ys[n - 1]))
    print("# Final impulse: %f %f" % (p_xs[n - 1], p_ys[n - 1]))
    print("# Final H: %f" % (H_list[n - 1]))
    runtime = time.time() - runtime
    print("# Total runtime = %3.2fs" % (runtime))
    print(
        "# --------------------------------------------------------------------------"
    )
    print("# --- Done with FUNCTION CALLS")
    # exit()

    #################### PLOTS: POSITION ####################

    n2 = int(n / 2)

    xs1 = xs[:n2]
    ys1 = ys[:n2]
    xs2 = xs[n2:]
    ys2 = ys[n2:]

    X_list1 = xs[:n2] * np.cos(ts[:n2]) - ys[:n2] * np.sin(ts[:n2])
    Y_list1 = xs[:n2] * np.sin(ts[:n2]) + ys[:n2] * np.cos(ts[:n2])
    X_list2 = xs[n2:] * np.cos(ts[n2:]) - ys[n2:] * np.sin(ts[n2:])
    Y_list2 = xs[n2:] * np.sin(ts[n2:]) + ys[n2:] * np.cos(ts[n2:])

    X_list_earth = EARTH_POSITION_X * np.cos(ts)
    Y_list_earth = -EARTH_POSITION_X * np.sin(ts)

    X_list_moon = LUNAR_POSITION_X * np.cos(ts)
    Y_list_moon = LUNAR_POSITION_X * np.sin(ts)

    # Rel. step_error
    plt.figure()
    plt.plot(ts * UNIT_TIME, step_errors)
    plt.xlabel("time (days)")
    plt.ylabel("step error")
    plt.yscale("log")
    plt.savefig(
        OUTPUT_DIR + "{}-step_error_vs_time.{}".format(MODE_NAME, FORMAT),
        bbox_inches="tight",
    )

    # Step sizes
    plt.figure()
    plt.plot(ts * UNIT_TIME, h_list)
    plt.xlabel("time (days)")
    plt.ylabel("step size")
    plt.yscale("log")
    plt.savefig(
        OUTPUT_DIR + "{}-step_size_vs_time.{}".format(MODE_NAME, FORMAT),
        bbox_inches="tight",
    )

    # Old and weird "Total energy error"
    # # Total energy error
    # H_avg = np.sum(H_list) / n
    # H_relative_errors = (H_list - H_avg) / H_avg
    # plt.figure()
    # plt.plot(ts * UNIT_TIME, H_relative_errors)
    # plt.xlabel("time (days)")
    # plt.ylabel("Hamiltonian relative error (arbitrary units)")
    # plt.savefig(
    #     OUTPUT_DIR + "{}-energy_error_vs_time.{}".format(MODE_NAME, FORMAT),
    #     bbox_inches="tight",
    # )

    # Total energy
    plt.figure()
    plt.plot(ts * UNIT_TIME, H_list)
    plt.xlabel("time (days)")
    plt.ylabel("Hamiltonian (arbitrary units)")
    plt.savefig(
        OUTPUT_DIR + "{}-energy_vs_time.{}".format(MODE_NAME, FORMAT),
        bbox_inches="tight",
    )

    # Zoom earth
    xlim = 0.02
    ylim = 0.02
    xmin = EARTH_POSITION_X - xlim
    xmax = EARTH_POSITION_X + xlim
    ymin = -ylim
    ymax = ylim
    plt.figure()
    earth = plt.Circle((EARTH_POSITION_X, 0), EARTH_RADIUS / UNIT_LENGTH, color="blue")
    earthorbit1 = plt.Circle(
        (EARTH_POSITION_X, 0),
        (LEO_RADIUS - ORBITAL_TOLERANCE) / UNIT_LENGTH,
        color="g",
        fill=False,
    )
    earthorbit2 = plt.Circle(
        (EARTH_POSITION_X, 0),
        (LEO_RADIUS + ORBITAL_TOLERANCE) / UNIT_LENGTH,
        color="g",
        fill=False,
    )
    plt.gcf().gca().add_artist(earth)
    plt.gcf().gca().add_artist(earthorbit1)
    plt.gcf().gca().add_artist(earthorbit2)
    plt.plot(xs1, ys1, "r-")
    plt.plot(xs2, ys2, "k-")
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.xlabel("x-position (arbitrary units)")
    plt.ylabel("y-position (arbitrary units)")
    plt.savefig(
        OUTPUT_DIR + "{}-earth_exit_y(x).{}".format(MODE_NAME, FORMAT),
        bbox_inches="tight",
    )

    # Zoom moon
    xlim = 0.0055
    ylim = 0.0055
    xmin = LUNAR_POSITION_X - xlim
    xmax = LUNAR_POSITION_X + xlim
    ymin = -ylim
    ymax = ylim
    plt.figure()
    moon = plt.Circle((LUNAR_POSITION_X, 0), LUNAR_RADIUS / UNIT_LENGTH, color="grey")
    moonorbit1 = plt.Circle(
        (LUNAR_POSITION_X, 0),
        (LLO_RADIUS - ORBITAL_TOLERANCE) / UNIT_LENGTH,
        color="g",
        fill=False,
    )
    moonorbit2 = plt.Circle(
        (LUNAR_POSITION_X, 0),
        (LLO_RADIUS + ORBITAL_TOLERANCE) / UNIT_LENGTH,
        color="g",
        fill=False,
    )
    plt.gcf().gca().add_artist(moon)
    plt.gcf().gca().add_artist(moonorbit1)
    plt.gcf().gca().add_artist(moonorbit2)
    plt.plot(xs1, ys1, "r-")
    plt.plot(xs2, ys2, "k-")
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.xlabel("x-position (arbitrary units)")
    plt.ylabel("y-position (arbitrary units)")
    plt.savefig(
        OUTPUT_DIR + "{}-moon_entry_y(x).{}".format(MODE_NAME, FORMAT),
        bbox_inches="tight",
    )

    # View center of mass
    xlim = 1.3
    ylim = 1.3
    xmin = -xlim
    xmax = xlim
    ymin = -ylim
    ymax = ylim

    # Position plot (X,Y)
    plt.figure()
    plt.plot(X_list1, Y_list1, "r")
    plt.plot(X_list2, Y_list2, "k")
    plt.plot(X_list_earth, Y_list_earth, "blue")
    plt.plot(X_list_moon, Y_list_moon, "grey")
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.xlabel("x-position (arbitrary units)")
    plt.ylabel("y-position (arbitrary units)")
    plt.savefig(
        OUTPUT_DIR + "{}-Y(X)_inertial.{}".format(MODE_NAME, FORMAT),
        bbox_inches="tight",
    )

    # Position plot (x,y)
    plt.figure()
    plt.plot(xs1, ys1, "r-")
    plt.plot(xs2, ys2, "k-")
    earth = plt.Circle((EARTH_POSITION_X, 0), EARTH_RADIUS / UNIT_LENGTH, color="blue")
    earthorbit1 = plt.Circle(
        (EARTH_POSITION_X, 0),
        (LEO_RADIUS - ORBITAL_TOLERANCE) / UNIT_LENGTH,
        color="g",
        fill=False,
    )
    earthorbit2 = plt.Circle(
        (EARTH_POSITION_X, 0),
        (LEO_RADIUS + ORBITAL_TOLERANCE) / UNIT_LENGTH,
        color="g",
        fill=False,
    )
    moon = plt.Circle((LUNAR_POSITION_X, 0), LUNAR_RADIUS / UNIT_LENGTH, color="grey")
    moonorbit1 = plt.Circle(
        (LUNAR_POSITION_X, 0),
        (LLO_RADIUS - ORBITAL_TOLERANCE) / UNIT_LENGTH,
        color="g",
        fill=False,
    )
    moonorbit2 = plt.Circle(
        (LUNAR_POSITION_X, 0),
        (LLO_RADIUS + ORBITAL_TOLERANCE) / UNIT_LENGTH,
        color="g",
        fill=False,
    )
    plt.gcf().gca().add_artist(earth)
    plt.gcf().gca().add_artist(earthorbit1)
    plt.gcf().gca().add_artist(earthorbit2)
    plt.gcf().gca().add_artist(moon)
    plt.gcf().gca().add_artist(moonorbit1)
    plt.gcf().gca().add_artist(moonorbit2)
    plt.plot(L1_POSITION_X, 0, "gx")
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.xlabel("x-position (arbitrary units)")
    plt.ylabel("y-position (arbitrary units)")
    plt.savefig(
        OUTPUT_DIR + "{}-y(x)_corotating.{}".format(MODE_NAME, FORMAT),
        bbox_inches="tight",
    )
    # plt.savefig('r3b/r3b_y(x)_euler_symplectic.{}',MODE_NAME, FORMAT='tight')
    # plt.show()
    plt.close()
    print("# --- Done with PLOTS")

    # # #################### PLOTS: VELOCITY ####################

    # plt.figure()
    # plt.plot(ts, omegalist_e)
    # plt.xlabel("time (arbitrary units)")
    # plt.ylabel("velocity (arbitrary units)")
    # plt.savefig('r3b/r3b_omega(t)_euler_explicit.{}')
    # # plt.MODE_NAME, FORMATow()
    # plt.close()

    # #################### PHASE-SPACE TRAJECTORY PLOTS ####################

    # # Explicit Euler phase-space trajectory
    # plt.figure()
    # plt.plot(thetalist_e[:len(thetalist_e)/2], omegalist_e[:len(omegalist_e)/2], 'r')
    # plt.plot(thetalist_e[len(thetalist_e)/2:], omegalist_e[len(omegalist_e)/2:], 'b')
    # plt.xlabel("position (arbitrary units)")
    # plt.ylabel("velocity (arbitrary units)")
    # plt.savefig('r3b/r3b_phase-space_euler_explicit.{}',MODE_NAME, FORMAT='tight')
    # #plt.show()
    # plt.close()

    # # Implicit Euler phase-space trajectory
    # plt.figure()
    # plt.plot(thetalist_i[:len(thetalist_i)/2], omegalist_i[:len(omegalist_i)/2], 'r')
    # plt.plot(thetalist_i[len(thetalist_i)/2:], omegalist_i[len(omegalist_i)/2:], 'b')
    # plt.xlabel("position (arbitrary units)")
    # plt.ylabel("velocity (arbitrary units)")
    # plt.savefig('r3b/r3b_phase-space_euler_implicit.{}',MODE_NAME, FORMAT='tight')
    # #plt.show()
    # plt.close()

    # # Symplectic Euler phase-space trajectory
    # plt.figure()
    # plt.plot(thetalist[:len(thetalist)/2], omegalist[:len(omegalist)/2], 'r')
    # plt.plot(thetalist[len(thetalist)/2:], omegalist[len(omegalist)/2:], 'b')
    # plt.xlabel("position (arbitrary units)")
    # plt.ylabel("velocity (arbitrary units)")
    # plt.savefig('r3b/r3b_phase-space_euler_symplectic.{}',MODE_NAME, FORMAT='tight')
    # #plt.show()
    # plt.close()

    # print("--- Done with PHASE-SPACE TRAJECTORY PLOTS")

    sys.stdout = old_stdout
    log_file.close()


if __name__ == "__main__":
    run_test()
