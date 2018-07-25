import matplotlib.pyplot as plt
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

    ax.scatter(xs[-0], ys[0], color="green")
    ax.scatter(xs[-1], ys[-1], len(hs), color="red")

    plt.show()


def orbitplot2d(completed_path):
    pass
