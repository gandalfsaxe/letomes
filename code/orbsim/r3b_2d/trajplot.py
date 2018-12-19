from math import cos, pi, sin, sqrt

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib import animation

import numpy as np

from . import *
from orbsim.r3b_2d.simulators import run_sim
from matplotlib.animation import ImageMagickFileWriter

EARTH_POSITION_X = -0.001
LUNAR_POSITION_X = 1


class TrajPlot(object):
    def __init__(self, completed_path, ax, inertial_mode = True):
        self.score, _, self.path = completed_path  # [Dv,success?,[x,y,px,py,h]]
        xs, ys, _, _, hs, ts = np.array(self.path).T
        self.ani_ax = ax
        self.idxs = get_idxs(hs)

        if inertial_mode:
            self.xs_traj = xs
            self.ys_traj = ys
        else:
            self.xs_traj = xs * np.cos(ts) - ys * np.sin(ts)
            self.ys_traj = xs * np.sin(ts) + ys * np.cos(ts)

        self.xs_earth = EARTH_POSITION_X * np.cos(ts)
        self.ys_earth = EARTH_POSITION_X * np.sin(ts)

        self.xs_moon = LUNAR_POSITION_X * np.cos(ts)
        self.ys_moon = LUNAR_POSITION_X * np.sin(ts)

        self.earth_xdata = [self.xs_earth[0]]
        self.earth_ydata = [self.ys_earth[0]]
        self.earth_line, = self.ani_ax.plot(
            self.earth_xdata, self.earth_ydata, color="red"
        )

        self.moon_xdata = [self.xs_moon[0]]
        self.moon_ydata = [self.ys_moon[0]]
        self.moon_line, = self.ani_ax.plot(
            self.moon_xdata, self.moon_ydata, color="green"
        )

        self.traj_xdata = [self.xs_traj[0]]
        self.traj_ydata = [self.ys_traj[0]]
        self.traj_line, = self.ani_ax.plot(
            self.traj_xdata, self.traj_ydata, color="black"
        )
        self.ani_ax.set_xlim((-1, 1))
        self.ani_ax.set_ylim((-1, 1))

        self.ani_terminate = False

    def update(self, i):
        if self.ani_terminate:
            return self.traj_line, self.earth_line, self.moon_line
        if i == len(self.xs_traj) - 1:
            self.ani_ax.scatter(self.xs_traj[-1], self.ys_traj[-1], color="black")
            self.ani_ax.scatter(
                self.xs_earth[-1],
                self.ys_earth[-1],
                self.zs_earth[-1],
                color="deepskyblue",
            )
            self.ani_ax.scatter(self.xs_moon[-1], self.ys_moon[-1], color="grey")
            self.ani_terminate = True
        x = self.xs_traj[self.idxs[i]]
        y = self.ys_traj[self.idxs[i]]
        self.traj_xdata.append(x)
        self.traj_ydata.append(y)
        self.traj_line.set_data(self.traj_xdata, self.traj_ydata)

        self.earth_xdata.append(self.xs_earth[self.idxs[i]])
        self.earth_ydata.append(self.ys_earth[self.idxs[i]])
        self.earth_line.set_data(self.earth_xdata, self.earth_ydata)
        
        self.moon_xdata.append(self.xs_moon[self.idxs[i]])
        self.moon_ydata.append(self.ys_moon[self.idxs[i]])
        self.moon_line.set_data(self.moon_xdata, self.moon_ydata)
        return self.traj_line, self.earth_line, self.moon_line


def get_idxs(hs):
    idxs = []
    tally = 0
    for i in range(
        len(hs)
    ):  # each time step h, check whether the little tally has reached our threshold.
        h = hs[i]  # if it has, take that index as a time step
        tally += h
        if tally >= 1.5e-3:
            idxs.append(i)
            tally = 0
    return idxs


if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.gca()
    cpath = run_sim([3.0, 0.0, 3.1], duration=50)
    trajp = TrajPlot(cpath, ax)
    ani = animation.FuncAnimation(
        fig, trajp.update, range(len(trajp.idxs)), interval=0.3, blit=True
    )
    plt.rcParams[
        "animation.convert_path"
    ] = "C:\Program Files\ImageMagick-7.0.8-Q16\magick.exe"  # "/usr/local/bin/magick"
    writer = ImageMagickFileWriter(fps=30)
    ani.save(f"{str(Path.home())}/animation.mp4", writer=writer)
    # plt.show()