import time

from orbsim.r3b_2d import *
from orbsim.plotting import orbitplot2d, orbitplot_non_inertial
from orbsim.r3b_2d.simulators import launch_sim
from argparse import ArgumentParser


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "paths",
        metavar="trajectories",
        type=str,
        nargs="+",
        help='the premade paths you want to check. options are "leo, llo, h, rh, ls, ll, 3h, 1h".',
    )
    args = parser.parse_args()
    paths = args.paths
    # for x in range(10):
    #     psi = [rand() *2*pi, rand() * 2* pi, rand() * 4 / unit_velocity]
    #     path = launch_sim(psi)
    #     orbitplot2d(path, psi)
    # starttime=time.time()
    # psi = [-2.282942228154665, 0.0000, -31.49483130653266 / unit_velocity]
    # launch_sim(psi,max_iter=1000000)
    # print(round(time.time() - starttime, 3))

    starttime = time.time()
    if "leo" in paths:
        # leo
        psi = [0.0, 0.0, 0.0]
        path = launch_sim(psi, duration=1 / UNIT_TIME)
        orbitplot2d(path, psi, title="leo")

    if "h" in paths:
        # hohmann
        psi = [
            -2.086814820119193,
            -0.000122173047640,
            3.111181716545691 / UNIT_VELOCITY,
        ]
        path = launch_sim(psi, duration=5 / UNIT_TIME)
        orbitplot2d(path, psi, title="hohmann")
        orbitplot_non_inertial(path, psi, title="hohmann")

    if "rh" in paths:
        # reverse hohmann
        psi = [
            -2.282942228154665,
            0.000000000000000,
            -3.149483130653266 / UNIT_VELOCITY,
        ]
        path = launch_sim(psi, duration=4 / UNIT_TIME)
        orbitplot2d(path, psi, title="reverse hohmann")
        orbitplot_non_inertial(path, psi, title="reverse_hohmann")

    if "ll" in paths:
        # low energy long
        psi = [3.794182930145708, 0.023901745288554, 3.090702702702703 / UNIT_VELOCITY]
        path = launch_sim(psi, duration=200 / UNIT_TIME)
        orbitplot2d(path, psi, title="LE long")
        orbitplot_non_inertial(path, psi, title="LE long")

    if "ls" in paths:
        # low energy short
        psi = [
            -0.138042744751570,
            -0.144259374836607,
            3.127288444444444 / UNIT_VELOCITY,
        ]
        path = launch_sim(psi, duration=41 / UNIT_TIME)
        orbitplot2d(path, psi, title="LE short")
        orbitplot_non_inertial(path, psi, title="LE short")

    if "3h" in paths:
        # 3-day-hohmann
        psi = [
            -2.272183066647597,
            -0.075821466029764,
            3.135519748743719 / UNIT_VELOCITY,
        ]
        path = launch_sim(psi, duration=3 / UNIT_TIME)
        orbitplot2d(path, psi, title="3-day-hohmann")
        orbitplot_non_inertial(path, psi, title="3-day-hohmann")

    if "1h" in paths:
        # 1-day-hohmann
        psi = [-2.277654673852600, 0.047996554429844, 3.810000000000000 / UNIT_VELOCITY]
        path = launch_sim(psi, duration=1 / UNIT_TIME)
        orbitplot2d(path, psi, title="1-day-hohmann")
        orbitplot_non_inertial(path, psi, title="1-day-hohmann")

    print(round(time.time() - starttime, 3))
