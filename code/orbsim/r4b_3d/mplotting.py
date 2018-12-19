from pathlib import Path

import matplotlib

matplotlib.use("Qt5Agg")

import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import ImageMagickFileWriter
import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3D

from orbsim.r4b_3d import UNIT_TIME
from orbsim.r4b_3d.coordinate_system import get_position_cartesian_from_spherical
from orbsim.r4b_3d.ephemerides import get_ephemerides, get_ephemerides_on_day


def all_plots_r4b_orbitplot(qs, ts, t_final, max_year):
    fig = plt.figure()
    ax1 = fig.add_subplot("221", projection="3d")
    ax2 = fig.add_subplot("222", projection="3d")
    ax3 = fig.add_subplot("223", projection="3d")
    for ax in [ax1, ax2, ax3]:
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
    r4b_orbit = R4bOrbit(qs, ts, t_final, max_year, ax1)
    r4b_orbit.zoom_orbit(ax2)
    r4b_orbit.r4b_orbitplot(ax3)
    # exit(0)
    # ani = animation.FuncAnimation(
    #     fig, r4b_orbit.update, range(len(qs)), interval=20, blit=False
    # )  # Turn off blitting if you want to rotate the plot. Turn it on if you wanna go fast
    # plt.rcParams[
    #     "animation.convert_path"
    # ] = "C:\Program Files\ImageMagick-7.0.8-Q16\magick.exe"  # "/usr/local/bin/magick"
    # writer = ImageMagickFileWriter()
    # ani.save(f"{str(Path.home())}/animation.mp4", writer=writer)

    plt.show()


class R4bOrbit(object):
    def __init__(self, qs, ts, t_final, max_year, ax):
        eph = get_ephemerides(max_year=max_year)
        earth = eph["earth"]
        mars = eph["mars"]
        # ts is in years, and is as such very small. we scale it to days, to fit with eph
        days_ts = [(t * UNIT_TIME) / 3600 / 24 for t in ts]

        qs = [get_position_cartesian_from_spherical(x, y, z) for x, y, z in qs]
        self.xs, self.ys, self.zs = np.array(
            qs
        ).T  # get individual coordinate sets for plotting

        self.t_final = t_final
        ax.set_title("animation")

        self.ani_ax = ax

        xs_earth = []
        ys_earth = []
        zs_earth = []
        xs_mars = []
        ys_mars = []
        zs_mars = []
        for t in days_ts:
            t_eph = get_ephemerides_on_day(eph, day_index=t)
            xs_earth.append(t_eph["earth"]["x"])
            ys_earth.append(t_eph["earth"]["y"])
            zs_earth.append(t_eph["earth"]["z"])
            xs_mars.append(t_eph["mars"]["x"])
            ys_mars.append(t_eph["mars"]["y"])
            zs_mars.append(t_eph["mars"]["z"])

        self.xs_earth = xs_earth
        self.ys_earth = ys_earth
        self.zs_earth = zs_earth

        self.xs_mars = xs_mars
        self.ys_mars = ys_mars
        self.zs_mars = zs_mars

        self.earth_xdata = [self.xs_earth[0]]
        self.earth_ydata = [self.ys_earth[0]]
        self.earth_zdata = [self.zs_earth[0]]
        self.earth_line = Line3D(
            self.earth_xdata, self.earth_ydata, self.earth_zdata, color="deepskyblue"
        )
        self.ani_ax.add_line(self.earth_line)

        self.mars_xdata = [self.xs_mars[0]]
        self.mars_ydata = [self.ys_mars[0]]
        self.mars_zdata = [self.zs_mars[0]]
        self.mars_line = Line3D(
            self.mars_xdata, self.mars_ydata, self.mars_zdata, color="orange"
        )
        self.ani_ax.add_line(self.mars_line)

        self.xdata = [self.xs[0]]
        self.ydata = [self.ys[0]]
        self.zdata = [self.zs[0]]
        self.traj_line = Line3D(self.xdata, self.ydata, self.zdata, color="black")
        self.ani_ax.add_line(self.traj_line)
        # -- SUN --
        ax.scatter(0, 0, 0, c="gold", marker="o")

        self.ani_ax.set_xlim(-1.5, 1.5)
        self.ani_ax.set_ylim(-1.5, 1.5)
        self.ani_ax.set_zlim(-1, 1)

        self.ani_terminate = False

    def update(self, i):
        if self.ani_terminate:
            return self.traj_line, self.earth_line, self.mars_line
        if i == len(self.xs) - 1:
            self.ani_ax.set_title("animation... DONE")
            self.ani_ax.scatter(self.xs[-1], self.ys[-1], self.zs[-1], color="black")
            self.ani_ax.scatter(
                self.xs_earth[-1],
                self.ys_earth[-1],
                self.zs_earth[-1],
                color="deepskyblue",
            )
            self.ani_ax.scatter(
                self.xs_mars[-1], self.ys_mars[-1], self.zs_mars[-1], color="orange"
            )
            self.ani_terminate = True
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

    def r4b_orbitplot(self, ax):

        ax.set_title("static holistic plot")

        ax.plot(self.xs, self.ys, self.zs, color="black")

        # -- EARTH --
        ax.plot(
            self.xs_earth, self.ys_earth, self.zs_earth, color="deepskyblue"
        )  # plot lines

        # -- MARS --
        ax.plot(self.xs_mars, self.ys_mars, self.zs_mars, color="orange")  # plot lines

        # -- SUN --

        ax.scatter(self.xs[-1], self.ys[-1], self.zs[-1], color="black")
        ax.scatter(
            self.xs_earth[-1], self.ys_earth[-1], self.zs_earth[-1], color="deepskyblue"
        )
        ax.scatter(self.xs_mars[-1], self.ys_mars[-1], self.zs_mars[-1], color="orange")
        ax.scatter(0, 0, 0, c="gold", marker="o")

    def zoom_orbit(self, ax):
        """orbit without mars, so we can see earth and spaceship trajectory as they move through space together."""
        earth_zoomline = Line3D(
            list(self.xs_earth),
            list(self.ys_earth),
            list(self.zs_earth),
            color="deepskyblue",
        )
        traj_zoomline = Line3D(self.xs, self.ys, self.zs, color="black")
        ax.set_title("zoomed in to spaceship")
        ax.scatter(0, 0, 0, c="gold", marker="o")  # Sun
        ax.add_line(earth_zoomline)
        ax.add_line(traj_zoomline)
        ax.set_xlim(min(self.xs), max(self.xs))
        ax.set_ylim(min(self.ys), max(self.ys))
        ax.set_zlim(min(self.zs), max(self.zs))
