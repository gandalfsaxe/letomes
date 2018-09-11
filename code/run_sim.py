import time

from orbsim.r3b_2d import *
from orbsim.plotting import orbitplot2d, orbitplot_non_inertial, leo_plot
from orbsim.r3b_2d.simulators import launch_sim
from argparse import ArgumentParser


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-p",
        metavar="paths",
        type=str,
        nargs="+",
        help='the premade paths you want to check. options are "leo, llo, h, rh, ls, ll, 3h, 1h".',
    )
    parser.add_argument(
        "--psi",
        metavar="in_psi",
        type=float,
        nargs="+",
        help="the position, angle and burn magnitude you want to simulate",
    )
    args = parser.parse_args()
    paths = args.p
    in_psi = args.psi
    # for x in range(10):
    #     psi = [rand() *2*pi, rand() * 2* pi, rand() * 4 / unit_velocity]
    #     path = launch_sim(psi)
    #     orbitplot2d(path, psi)
    # starttime=time.time()
    # psi = [-2.282942228154665, 0.0000, -31.49483130653266 / unit_velocity]
    # launch_sim(psi,max_iter=1000000)
    # print(round(time.time() - starttime, 3))

    starttime = time.time()
    if in_psi is not None and len(in_psi) == 3:
        # user defined
        psi = in_psi
        path = launch_sim(psi, duration=100)
        orbitplot2d(path, psi, title="userdef")
        orbitplot_non_inertial(path, psi, title="userdef")
    if paths is not None:
        if "leo" in paths:
            # leo
            psi = [0.0, 0.0, 0.0]
            path = launch_sim(psi, duration=0.0625)
            leo_plot(path, psi, title="leo")

        if "h" in paths:
            # hohmann
            psi = [-2.086814820119193, -0.000122173047640, 3.111181716545691]
            path = launch_sim(psi, duration=5)
            orbitplot2d(path, psi, title="hohmann")
            orbitplot_non_inertial(path, psi, title="hohmann")

        if "rh" in paths:
            # reverse hohmann
            psi = [-2.282942228154665, 0.000000000000000, -3.149483130653266]
            path = launch_sim(psi, duration=1)
            orbitplot2d(path, psi, title="reverse hohmann")
            orbitplot_non_inertial(path, psi, title="reverse_hohmann")

        if "ll" in paths:
            # low energy long
            psi = [3.794182930145708, 0.023901745288554, 3.090702702702703]
            path = launch_sim(psi, duration=200)
            orbitplot2d(path, psi, title="LE long")
            orbitplot_non_inertial(path, psi, title="LE long")

        if "ls" in paths:
            # low energy short
            psi = [-0.138042744751570, -0.144259374836607, 3.127288444444444]
            path = launch_sim(psi, duration=41)
            orbitplot2d(path, psi, title="LE short")
            orbitplot_non_inertial(path, psi, title="LE short")

        if "3h" in paths:
            # 3-day-hohmann
            psi = [-2.272183066647597, -0.075821466029764, 3.135519748743719]
            path = launch_sim(psi, duration=3)
            orbitplot2d(path, psi, title="3-day-hohmann")
            orbitplot_non_inertial(path, psi, title="3-day-hohmann")

        if "1h" in paths:
            # 1-day-hohmann
            psi = [-2.277654673852600, 0.047996554429844, 3.810000000000000]
            path = launch_sim(psi, duration=1)
            orbitplot2d(path, psi, title="1-day-hohmann")
            orbitplot_non_inertial(path, psi, title="1-day-hohmann")

    print(round(time.time() - starttime, 3))
