from math import cos, pi, sin, sqrt

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from .planets import celestials
from .r3b_2d import *


def orbitplot2d(completed_path, psi=None, filepath=".", title=None, multi_mode=False):

    """
    input: output of launch_sim, its launch parameters, and an optional title if the file is to be saved
    
    Plots a figure of the inputted orbit, with start point marked in green, and point marked in red, earth and moon/mars marked as well.
    """
    score, _, path = completed_path  # [Dv,success?,[x,y,px,py,h]]

    xs, ys, pxs, pys, hs, ts = np.array(path).T

    Xs = xs * np.cos(ts) - ys * np.sin(ts)
    Ys = xs * np.sin(ts) + ys * np.cos(ts)

    Xs_earth = EARTH_POSITION_X * np.cos(ts)
    Ys_earth = EARTH_POSITION_X * np.sin(ts)

    Xs_moon = LUNAR_POSITION_X * np.cos(ts)
    Ys_moon = LUNAR_POSITION_X * np.sin(ts)

    idxs = get_idxs(ts)
    N_PTS = len(idxs)
    increment = int(N_PTS/100)

    if multi_mode:
        ax = plt.gca()
    else:
        fig, ax = fig_setup(score, psi)
        cm = plt.get_cmap("bone")
        ax.set_prop_cycle(
            "color",
            [
                cm(max(0,0.9 - (1. * i / (N_PTS / increment))))
                for i in range(int(N_PTS / increment))
            ],
        )

    g_Xs, g_Ys = np.array([[Xs[idx], Ys[idx]] for idx in idxs]).T
    for i in range(N_PTS)[::increment]:
        ax.plot(g_Xs[i : i + increment], g_Ys[i : i + increment], linewidth=1)

    ax.plot(Xs_earth, Ys_earth, color="grey", linewidth=0.5, alpha=0.8)
    ax.plot(Xs_moon, Ys_moon, color="grey", linewidth=0.5)

    circle_x, circle_y = orbital_circle(celestials.MOON)
    ax.plot(circle_x, circle_y, color="grey", linewidth=0.3, alpha=0.6)

    earth = plt.Circle(
        (Xs_earth[0], Ys_earth[0]), EARTH_RADIUS / UNIT_LENGTH, color="blue", alpha=0.8
    )
    moon = plt.Circle(
        (Xs_moon[-1], Ys_moon[-1]), LUNAR_RADIUS / UNIT_LENGTH, color="grey", alpha=0.8
    )
    ax.add_artist(earth)
    ax.add_artist(moon)

    # ax.scatter(Xs[0], Ys[0], color="green")
    ax.scatter(Xs[-1], Ys[-1], color="red", marker="x", linewidth=0.6)

    if not multi_mode:
        if title is None:
            plt.show()
        else:
            filename = f"{filepath}/path_{title}.pdf"
            plt.savefig(filename)


def orbitplot_non_inertial(
    completed_path, psi=None, filepath=".", title=None, multi_mode=False
):
    """
    input: output of launch_sim, its launch parameters, and an optional title if the file is to be saved
    
    Plots a figure of the inputted orbit in the non-inertial reference frame, with end point marked in red, earth and moon/mars marked as well.
    """
    score, path = completed_path  # [Dv,[x,y,px,py,h]]

    xs, ys, pxs, pys, hs, _ = np.array(path).T

    idxs = get_idxs(hs)
    N_PTS = len(idxs)
    increment = int(N_PTS/100)
    if multi_mode:
        ax = plt.gca()
    else:
        fig, ax = fig_setup(score, psi)
        cm = plt.get_cmap("bone")
        ax.set_prop_cycle(
            "color",
            [
                cm(max(0,0.9 - (1. * i / (N_PTS / increment))))
                for i in range(int(N_PTS / increment))
            ],
        )

    g_xs, g_ys = np.array([[xs[idx], ys[idx]] for idx in idxs]).T
    for i in range(N_PTS)[::increment]:
        ax.plot(g_xs[i : i + increment], g_ys[i : i + increment], linewidth=1)

    earth = plt.Circle((EARTH_POSITION_X, 0), EARTH_RADIUS / UNIT_LENGTH, color="blue")
    moon = plt.Circle((LUNAR_POSITION_X, 0), LUNAR_RADIUS / UNIT_LENGTH, color="grey")
    ax.add_artist(earth)
    ax.add_artist(moon)

    ax.scatter([L1_POSITION_X], [0], marker="x", color="pink", linewidth=0.4)
    ax.scatter(xs[-1], ys[-1], color="red", marker="x", linewidth=0.6)

    circle_x, circle_y = orbital_circle(celestials.MOON)
    ax.plot(circle_x, circle_y, color="grey", linewidth=0.3, alpha=0.3)

    if not multi_mode:
        if title is None:
            plt.show()
        else:
            filename = f"{filepath}/path_{title}_non-inertial.pdf"
            plt.savefig(filename)


def get_idxs(hs):
    idxs = []
    tally = 0
    for i in range(
        len(hs)
    ):  # each time step h, check whether the little tally has reached our threshold.
        h = hs[i]  # if it has, take that index as a time step
        tally += h
        if tally >= 1.5e-4:
            idxs.append(i)
            tally = 0
    return idxs


def fig_setup(score, psi):
    fig = plt.figure()
    ax = fig.gca()
    if score < 100:
        scorestr = "DeltaV"
    else:
        scorestr = "smallest distance"
    if psi is not None:
        fig.suptitle(f"{scorestr} = {score}, psi = {[round(p,3) for p in psi]}")
    else:
        fig.suptitle(f"{scorestr} = {score}")

    ax.set_aspect("equal")
    return fig, ax


def orbitplot3d(completed_path, psi, filepath=".", title=None):
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

    # ax.scatter(xs[-0], ys[0], color="green")
    ax.scatter(xs[-1], ys[-1], len(hs), color="red")

    plt.show()


def leo_plot(completed_path, psi=None, filepath=".", title=None, fig=None):
    """
    input: output of launch_sim, its launch parameters, and an optional title if the file is to be saved
    
    Plots a figure of the inputted orbit, with start point marked in green, and point marked in red, earth and moon/mars marked as well.
    """
    score, path = completed_path  # [Dv,[x,y,px,py,h]]
    xs, ys, pxs, pys, hs, ts = np.array(path).T
    # ts = np.linspace(0, sum(hs), len(path))

    increment = 500
    fig, ax = fig_setup(score, psi)

    ax.plot(xs, ys, color="black", linewidth="2")
    earth = plt.Circle((EARTH_POSITION_X, 0), EARTH_RADIUS / UNIT_LENGTH, color="blue")
    ax.add_artist(earth)

    if title is None:
        plt.show()
    else:
        filename = f"{filepath}/path_{title}.pdf"
        plt.savefig(filename)


def multi_plot(completed_paths, psis, plot_type, filepath=".", title=None):
    N = len(completed_paths)
    if len(psis) != N:
        raise Exception("must have the same number of psis as paths")
    fig = plt.figure()
    ax = plt.gca()
    ax.set_aspect("equal")
    cmap_cycle = ["bone", "autumn", "winter", "summer", "spring"]

    for i, [cpath, psi] in enumerate(zip(completed_paths, psis)):
        _, path = cpath
        ts = np.array(path).T[5]
        idxs = get_idxs(ts)
        increment = len(idxs)/100
        # print(len(idxs),increment)

        cm = plt.get_cmap(cmap_cycle[i % len(cmap_cycle)])
        ax.set_prop_cycle(
            "color",
            [cm(max(0,0.9 - (1. * i / 100))) for i in range(100)],
        )
        plot_type(cpath, psi, multi_mode=True)

    if title is None:
        plt.show()
    else:
        filename = f"{filepath}/path_{title}.pdf"
        plt.savefig(filename)
    plt.close()


def orbital_circle(celestial):
    """
    input: celestial enum
    returns: x/y points for a plottable circle of the celestial's orbit
    """
    if celestial == celestials.MOON:
        circle_x = [LUNAR_POSITION_X * cos(x / 100.0 * 2 * pi) for x in range(0, 101)]
        circle_y = [LUNAR_POSITION_X * sin(x / 100.0 * 2 * pi) for x in range(0, 101)]
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
