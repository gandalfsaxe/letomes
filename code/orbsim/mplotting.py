import pandas as pd

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3D
from matplotlib import animation, rc
from matplotlib.animation import ImageMagickFileWriter
from orbsim.r4b_3d.coordinate_system import get_position_cartesian_from_spherical
import matplotlib.pyplot as plt
import numpy as np
import os
import msvcrt as m
from pathlib import Path


FILE_PATH = "orbsim/r4b_3d/ephemerides/"
# FILE_PATH = "code/orbsim/r4b_3d/ephemerides/"

# FILENAME_EARTH = "earth_2019-2020.csv"
FILENAME_EARTH = "earth_2019-2039.csv"
# FILENAME_EARTH = "earth_2019-2262.csv"

# FILENAME_MARS = "mars_2019-2020.csv"
FILENAME_MARS = "mars_2019-2039.csv"
# FILENAME_MARS = "mars_2019-2262.csv"

# Change CWD if necessary
cwd = os.getcwd()
in_correct_cwd = (
    "code" + FILE_PATH[2:-1] == cwd[-30:]
)  # Check if last part of cwd is '/code/orbsim/r4b_3d'

if not in_correct_cwd:
    os.chdir(FILE_PATH)
    cwd = os.getcwd()

print(cwd)

# Read CSV files

earth = pd.read_csv(FILENAME_EARTH, parse_dates=["date"], index_col="day")
mars = pd.read_csv(FILENAME_MARS, parse_dates=["date"], index_col="day")

pd.set_option("max_row", 20)


def r4b_orbitplot(qs, ax):
    qs = [get_position_cartesian_from_spherical(x, y, z) for x, y, z in qs]
    xs, ys, zs = np.array(qs).T  # get individual coordinate sets for plotting

    ax.plot(xs, ys, zs, color="black")

    # -- EARTH --
    x = earth["x"][::8]
    y = earth["y"][::8]
    z = earth["z"][::8]
    # x = earth["x"]
    # y = earth["y"]
    # z = earth["z"]
    ax.plot(x, y, z, color="deepskyblue")  # plot lines

    # -- MARS --
    x = mars["x"][::8]
    y = mars["y"][::8]
    z = mars["z"][::8]
    # x = mars['x']
    # y = mars['y']
    # z = mars['z']
    ax.plot(x, y, z, color="orange")  # plot lines

    # -- SUN --
    ax.scatter(0, 0, 0, c="gold", marker="o")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")


def animate_r4b_orbitplot(qs, fig, ax):
    r4b_orbit = R4bOrbit(qs, ax)
    ani = animation.FuncAnimation(
        fig, r4b_orbit.update, range(len(qs)), interval=0.1, blit=True
    )  # Turn off blitting if you want to rotate the plot. Turn it on if you wanna go fast
    plt.rcParams[
        "animation.convert_path"
    ] = "C:\Program Files\ImageMagick-7.0.8-Q16\magick.exe"  # "/usr/local/bin/magick"
    writer = ImageMagickFileWriter()
    ani.save(f"{str(Path.home())}/animation.mp4", writer=writer)
    plt.show()


class R4bOrbit(object):
    def __init__(self, qs, ax):
        # ts, qs, ps, _, _ = traj
        qs = [get_position_cartesian_from_spherical(x, y, z) for x, y, z in qs]
        self.xs, self.ys, self.zs = np.array(
            qs
        ).T  # get individual coordinate sets for plotting

        self.ax = ax

        self.xs_earth = earth["x"]
        self.ys_earth = earth["y"]
        self.zs_earth = earth["z"]

        self.xs_mars = mars["x"]
        self.ys_mars = mars["y"]
        self.zs_mars = mars["z"]

        self.xdata = [self.xs[0]]
        self.ydata = [self.ys[0]]
        self.zdata = [self.zs[0]]
        self.traj_line = Line3D(self.xdata, self.ydata, self.zdata, color="black")
        self.ax.add_line(self.traj_line)

        self.earth_xdata = [self.xs_earth[0]]
        self.earth_ydata = [self.ys_earth[0]]
        self.earth_zdata = [self.zs_earth[0]]
        self.earth_line = Line3D(
            self.earth_xdata, self.earth_ydata, self.earth_zdata, color="deepskyblue"
        )
        self.ax.add_line(self.earth_line)

        self.mars_xdata = [self.xs_mars[0]]
        self.mars_ydata = [self.ys_mars[0]]
        self.mars_zdata = [self.zs_mars[0]]
        self.mars_line = Line3D(
            self.mars_xdata, self.mars_ydata, self.mars_zdata, color="orange"
        )
        self.ax.add_line(self.mars_line)

        # -- SUN --
        ax.scatter(0, 0, 0, c="gold", marker="o")

        self.ax.set_xlim(-1.5, 1.5)
        self.ax.set_ylim(-1.5, 1.5)
        self.ax.set_zlim(-1, 1)

    def update(self, i):
        # if i == len(self.xs) - 1:
        #     plt.close()
        x = self.xs[i]
        y = self.ys[i]
        z = self.zs[i]
        self.xdata.append(x)
        self.ydata.append(y)
        self.zdata.append(z)
        self.traj_line.set_data(self.xdata, self.ydata)
        self.traj_line.set_3d_properties(zs=self.zdata)

        self.earth_xdata.append(self.xs_earth[i])
        self.earth_ydata.append(self.ys_earth[i])
        self.earth_zdata.append(self.zs_earth[i])
        self.earth_line.set_data(self.earth_xdata, self.earth_ydata)
        self.earth_line.set_3d_properties(zs=self.earth_zdata)

        self.mars_xdata.append(self.xs_mars[i])
        self.mars_ydata.append(self.ys_mars[i])
        self.mars_zdata.append(self.zs_mars[i])
        self.mars_line.set_data(self.mars_xdata, self.mars_ydata)
        self.mars_line.set_3d_properties(zs=self.mars_zdata)
        return self.traj_line, self.earth_line, self.mars_line

