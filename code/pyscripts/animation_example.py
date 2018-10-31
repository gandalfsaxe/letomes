import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from orbsim.r3b_2d.simulators import run_sim
from orbsim.plotting import orbital_circle, get_idxs
from orbsim.planets import celestials
from orbsim.r3b_2d import *

import msvcrt as m


class Orbit(object):
    def __init__(self, path, ax, interval=32, inertial=False):
        # score, _, path = completed_path  # [Dv,success?,[x,y,px,py,h]]
        xs, ys, _, _, hs, ts = np.array(path).T
        self.inertial = inertial
        Xs = xs * np.cos(ts) - ys * np.sin(ts)
        Ys = xs * np.sin(ts) + ys * np.cos(ts)

        Xs_moon = LUNAR_POSITION_X * np.cos(ts)
        Ys_moon = LUNAR_POSITION_X * np.sin(ts)

        Xs_earth = EARTH_POSITION_X * np.cos(ts)
        Ys_earth = EARTH_POSITION_X * np.sin(ts)

        circle_x, circle_y = orbital_circle(celestials.MOON)
        ax.plot(circle_x, circle_y, color="grey", linewidth=0.3, alpha=0.6)
        ax.set_aspect(1)

        idxs = get_idxs(hs)

        if inertial:
            self.xs = Xs
            self.ys = Ys
        else:
            self.xs, self.ys = np.array([[xs[idx], ys[idx]] for idx in idxs])[
                ::interval
            ].T
            self.Xs_moon, self.Ys_moon = np.array(
                [[Xs_moon[idx], Ys_moon[idx]] for idx in idxs]
            )[::interval].T
            self.Xs_earth, self.Ys_earth = np.array(
                [[Xs_earth[idx], Ys_earth[idx]] for idx in idxs]
            )[::interval].T

        self.ax = ax
        self.xdata = [xs[0]]
        self.ydata = [ys[0]]
        self.line = Line2D(self.xdata, self.ydata, color="red")
        self.ax.add_line(self.line)

        self.lunxdata = [LUNAR_POSITION_X]
        self.lunydata = [0]
        self.moonline = Line2D(self.lunxdata, self.lunydata, color="grey")
        self.ax.add_line(self.moonline)

        self.earthxdata = [EARTH_POSITION_X]
        self.earthydata = [0]
        self.earthline = Line2D(self.earthxdata, self.earthydata, color="blue")
        self.ax.add_line(self.earthline)

        self.ax.set_ylim(-1.1, 1.1)
        self.ax.set_xlim(-1.1, 1.1)

    def update(self, i):
        if i == len(self.xs)-1:
            m.getch()
            exit()
        x = self.xs[i]
        y = self.ys[i]
        print(x, y, self.Xs_moon[i] ** 2 + self.Ys_moon[i] ** 2)
        self.xdata.append(x)
        self.ydata.append(y)
        self.line.set_data(self.xdata, self.ydata)

        self.lunxdata.append(self.Xs_moon[i])
        self.lunydata.append(self.Ys_moon[i])
        self.moonline.set_data(self.lunxdata, self.lunydata)
        return self.line, self.moonline


score, success, path = run_sim(
    [3.794182930145708, 0.023901745288554, 3.090702702702703], duration=50, max_iter=1e7
)
fig, ax = plt.subplots()
interval = 32
orbit = Orbit(path, ax, interval=interval)

# pass a generator in "emitter" to produce data for the update func
ani = animation.FuncAnimation(
    fig, orbit.update, range(int(len(path) / interval)), interval=5, blit=True
)

plt.show()
