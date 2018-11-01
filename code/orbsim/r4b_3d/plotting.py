import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pdir
from mpl_toolkits.mplot3d import Axes3D

from orbsim.r4b_3d import UNIT_TIME


def r4b_plot(t_final, ephemerides, qs):

    t_final_days = t_final * UNIT_TIME / 3600 / 24

    earth = ephemerides["earth"]
    mars = ephemerides["mars"]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    # -- EARTH --
    # x = earth['x'][::10]
    # y = earth['y'][::10]
    # z = earth['z'][::10]
    x = earth["x"]
    y = earth["y"]
    z = earth["z"]

    ax.scatter(0, 0, 0, c="gold", marker="o", s=200)

    # ax.plot3D(x, y, z, c='deepskyblue', marker='.')   # Plot dots + lines
    ax.scatter(x, y, z, c="deepskyblue", marker=".")  # plot dots
    # ax.plot(x,y,z, color='deepskyblue')               # plot lines

    # -- MARS --
    # x = mars['x'][::10]
    # y = mars['y'][::10]
    # z = mars['z'][::10]
    x = mars["x"]
    y = mars["y"]
    z = mars["z"]

    ax.scatter(0, 0, 0, c="gold", marker="o", s=200)

    # ax.plot3D(x, y, z, c='orange', marker='.')   # Plot dots + lines
    ax.scatter(x, y, z, c="orange", marker=".")  # plot dots
    # ax.plot(x,y,z, color='orange')               # plot lines

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    plt.show()
