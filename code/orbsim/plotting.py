from math import cos, sin

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from orbsim.constants import *


def orbitplot(completed_path):
    Dv, path = completed_path

    xs = [e[0] for e in path]
    ys = [e[1] for e in path]
    hs = [e[4] for e in path]
    fig = plt.figure()
    ax = fig.gca(projection="3d")
    fig.suptitle(f"DeltaV = {Dv}")

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


def orbitplot2d(completed_path, psi, title=None):
    Dv, path = completed_path

    xs = [e[0] for e in path]
    ys = [e[1] for e in path]
    hs = [e[4] for e in path]
    fig = plt.figure()
    ax = fig.gca()
    fig.suptitle(f"DeltaV = {Dv}")

    ax.plot(xs, ys, color="black", linewidth=2)
    ax.scatter([earth_position_x], [0], color="blue")
    ax.scatter([lunar_position_x], [0], color="grey")
    ax.scatter([L1_position_x], [0], color="pink")

    circle_x = [cos(x / 100.0 * 2 * pi) for x in range(100)]
    circle_y = [sin(x / 100.0 * 2 * pi) for x in range(100)]

    ax.plot(circle_x, circle_y, color="grey")

    ax.scatter(xs[-0], ys[0], color="green")
    ax.scatter(xs[-1], ys[-1], color="red")
    if title is None:
        filename = f"./path_{round(psi[0],2)};{round(psi[1],2)};{round(psi[2],2)}.png"
    else:
        filename = f"./path_{title}.png"
    plt.savefig(fname=filename)
