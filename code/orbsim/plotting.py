from math import cos, sin
from .planets import celestials

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from orbsim.constants import *


def orbitplot3d(completed_path, psi, title=None):
    Dv, path = completed_path

    xs = [e[0] for e in path]
    ys = [e[1] for e in path]
    hs = [e[4] for e in path]
    fig = plt.figure()
    ax = fig.gca(projection="3d")
    fig.suptitle(f"DeltaV = {Dv}, hyperparameters = {[round(p,3) for p in psi]}")

    ax.plot(xs, ys, range(len(hs)), color="black", linewidth=2)

    ax.scatter([earth_position_x], [0], color="blue")
    ax.scatter([lunar_position_x], [0], color="grey")
    ax.scatter([L1_position_x], [0], color="pink")

    circle_x = [cos(x / 100.0 * 2 * pi) for x in range(100)]
    circle_y = [sin(x / 100.0 * 2 * pi) for x in range(100)]

    ax.plot(circle_x, circle_y, color="grey")

    ax.scatter(xs[-0], ys[0], color="green")
    ax.scatter(xs[-1], ys[-1], len(hs), color="red")

    plt.show()


def orbitplot2d(completed_path, psi=None, title=None):
    '''
    input: output of launch_sim, its launch parameters, and an optional title if the file is to be saved
    
    Plots a figure of the inputted orbit, with start point marked in green, and point marked in red, earth and moon/mars marked as well.
    '''
    Dv, path = completed_path

    xs = [e[0] for e in path]
    ys = [e[1] for e in path]
    hs = [e[4] for e in path]
    fig = plt.figure()
    ax = fig.gca()
    if psi is not None:
        fig.suptitle(f"DeltaV = {Dv}, hyperparameters = {[round(p,3) for p in psi]}")
    else:
        fig.suptitle(f"DeltaV = {Dv}")

    ax.plot(xs, ys, color="black", linewidth=2)
    ax.scatter([earth_position_x], [0], color="blue")
    ax.scatter([lunar_position_x], [0], color="grey")
    ax.scatter([L1_position_x], [0], color="pink")

    circle_x, circle_y = orbital_circle(celestials.MOON)

    ax.plot(circle_x, circle_y, color="grey")

    ax.scatter(xs[-0], ys[0], color="green")
    ax.scatter(xs[-1], ys[-1], color="red")
    if title is None:
        plt.show()
    else:
        filename = f"./path_{title}.png"
        plt.savefig(fname=filename)


def orbital_circle(celestial):
    '''
    input: celestial enum
    returns: x/y points for a plottable circle of the celestial's orbit
    '''
    if celestial == celestials.MOON:
        circle_x = [cos(x / 100.0 * 2 * pi) for x in range(1, 101)]
        circle_y = [sin(x / 100.0 * 2 * pi) for x in range(1, 101)]
    elif celestial == celestials.MARS:
        circle_x = [
            mars_earth_distance * cos(x / 100.0 * 2 * pi) for x in range(1, 101)
        ]
        circle_y = [
            mars_earth_distance * sin(x / 100.0 * 2 * pi) for x in range(1, 101)
        ]
    elif celestial == celestials.EARTH:
        return None

    return [circle_x, circle_y]

