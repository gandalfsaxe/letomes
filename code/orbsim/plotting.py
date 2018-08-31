from math import cos, pi, sin, sqrt

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from .planets import celestials
from .r3b_2d import *


def orbitplot3d(completed_path, psi,  filepath=".", title=None):
    Dv, path = completed_path

    xs = [e[0] for e in path]
    ys = [e[1] for e in path]
    hs = [e[4] for e in path]
    fig = plt.figure()
    ax = fig.gca(projection="3d")
    fig.suptitle(f"DeltaV = {Dv}, hyperparameters = {[round(p,3) for p in psi]}")

    ax.plot(xs, ys, range(len(hs)), color="black", linewidth=2)

    ax.scatter([EARTH_POSITION_X], [0], color="blue")
    ax.scatter([LUNAR_POSITION_X], [0], color="grey")
    ax.scatter([L1_POSITION_X], [0], color="pink")

    circle_x = [cos(x / 100.0 * 2 * pi) for x in range(100)]
    circle_y = [sin(x / 100.0 * 2 * pi) for x in range(100)]

    ax.plot(circle_x, circle_y, color="grey")

    ax.scatter(xs[-0], ys[0], color="green")
    ax.scatter(xs[-1], ys[-1], len(hs), color="red")

    plt.show()


def leo_plot(completed_path, psi=None,  filepath=".", title=None):
    """
    input: output of launch_sim, its launch parameters, and an optional title if the file is to be saved
    
    Plots a figure of the inputted orbit, with start point marked in green, and point marked in red, earth and moon/mars marked as well.
    """
    Dv, path = completed_path  # [Dv,[x,y,px,py,h]]

    xs = [e[0] for e in path]
    ys = [e[1] for e in path]
    pxs = [e[2] for e in path]
    pys = [e[3] for e in path]
    hs = [e[4] for e in path]

    ts = np.linspace(0, sum(hs), len(path))

    fig = plt.figure()
    ax = fig.gca()
    if psi is not None:
        fig.suptitle(f"DeltaV = {Dv}, psi = {[round(p,3) for p in psi]}")
    else:
        fig.suptitle(f"DeltaV = {Dv}")

    ax.set_aspect("equal")

    ax.plot(xs, ys, color="black", linewidth="2")
    earth = plt.Circle((EARTH_POSITION_X, 0),EARTH_RADIUS/UNIT_LENGTH, color="blue")
    ax.add_artist(earth)

    # ax.scatter(xs[0], xs[0], color="green")
    # ax.scatter(xs[-1], xs[-1], color="red")

    if title is None:
        plt.show()
    else:
        filename = f"{filepath}/path_{title}.pdf"
        plt.savefig(filename)


def orbitplot2d(completed_path, psi=None, filepath=".",title=None):
    """
    input: output of launch_sim, its launch parameters, and an optional title if the file is to be saved
    
    Plots a figure of the inputted orbit, with start point marked in green, and point marked in red, earth and moon/mars marked as well.
    """
    Dv, path = completed_path  # [Dv,[x,y,px,py,h]]

    xs = [e[0] for e in path]
    ys = [e[1] for e in path]
    pxs = [e[2] for e in path]
    pys = [e[3] for e in path]
    hs = [e[4] for e in path]

    ts = np.linspace(0, sum(hs), len(path))

    Xs = xs * np.cos(ts) - ys * np.sin(ts)
    Ys = xs * np.sin(ts) + ys * np.cos(ts)

    Xs_earth = EARTH_POSITION_X * np.cos(ts)
    Ys_earth = EARTH_POSITION_X * np.sin(ts)

    Xs_moon = LUNAR_POSITION_X * np.cos(ts)
    Ys_moon = LUNAR_POSITION_X * np.sin(ts)

    Hs = [
        pxs[i] ** 2 / 2
        + pys[i] ** 2 / 2
        + ys[i] * pxs[i]
        - xs[i] * pys[i]
        - (1 - k) / sqrt((k + xs[i]) ** 2)
        + ys[i] ** 2
        - k / sqrt((1 - k - xs[i]) ** 2)
        + ys[i] ** 2
        for i in range(len(path))
    ]

    fig = plt.figure()
    ax = fig.gca()
    if psi is not None:
        fig.suptitle(f"DeltaV = {Dv}, psi = {[round(p,3) for p in psi]}")
    else:
        fig.suptitle(f"DeltaV = {Dv}")

    ax.set_aspect("equal")
    ax.plot(Xs, Ys, color="black", linewidth=2)
    ax.plot(Xs_earth, Ys_earth, color="blue", linewidth=1)
    ax.plot(Xs_moon, Ys_moon, color="grey", linewidth=0.5)

    ax.scatter(Xs[0], Ys[0], color="green")
    ax.scatter(Xs[-1], Ys[-1], color="red")

    if title is None:
        plt.show()
    else:
        filename = f"{filepath}/path_{title}.pdf"
        plt.savefig(filename)


def orbitplot_non_inertial(completed_path, psi=None,  filepath=".", title=None):
    """
    input: output of launch_sim, its launch parameters, and an optional title if the file is to be saved
    
    Plots a figure of the inputted orbit in the non-inertial reference frame, with start point marked in green, and point marked in red, earth and moon/mars marked as well.
    """
    Dv, path = completed_path  # [Dv,[x,y,px,py,h]]

    xs = [e[0] for e in path]
    ys = [e[1] for e in path]
    pxs = [e[2] for e in path]
    pys = [e[3] for e in path]
    hs = [e[4] for e in path]

    fig = plt.figure()
    ax = fig.gca()
    if psi is not None:
        fig.suptitle(f"DeltaV = {Dv}, psi = {[round(p,3) for p in psi]}")
    else:
        fig.suptitle(f"DeltaV = {Dv}")

    ax.plot(xs, ys, color="black", linewidth=2)
    ax.scatter([EARTH_POSITION_X], [0], color="blue")
    ax.scatter([LUNAR_POSITION_X], [0], color="grey")
    ax.scatter([L1_POSITION_X], [0], color="pink")

    circle_x, circle_y = orbital_circle(celestials.MOON)

    ax.set_aspect("equal")    
    ax.plot(circle_x, circle_y, color="grey")

    ax.scatter(xs[-0], ys[0], color="green")
    ax.scatter(xs[-1], ys[-1], color="red")
    if title is None:
        plt.show()
    else:
        filename = f"{filepath}/path_{title}_non-inertial.pdf"
        plt.savefig(filename)


def orbital_circle(celestial):
    """
    input: celestial enum
    returns: x/y points for a plottable circle of the celestial's orbit
    """
    if celestial == celestials.MOON:
        circle_x = [cos(x / 100.0 * 2 * pi) for x in range(1, 101)]
        circle_y = [sin(x / 100.0 * 2 * pi) for x in range(1, 101)]
    elif celestial == celestials.MARS:
        circle_x = [
            mars_orbital_distance * cos(x / 100.0 * 2 * pi) for x in range(1, 101)
        ]
        circle_y = [
            mars_orbital_distance * sin(x / 100.0 * 2 * pi) for x in range(1, 101)
        ]
    elif celestial == celestials.EARTH:
        return None

    return [circle_x, circle_y]
