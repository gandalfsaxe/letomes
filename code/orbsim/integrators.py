from .analyticals import *
from .constants import *
from .planets import *
import time
from numba import jit


@jit
def euler_step(h, x, y, p_x, p_y):
    """takes a single time step of the symplectic euler algorithm"""
    v_x = p_x + y
    x = (x + h * (v_x + p_y * h)) / (1.0 + h ** 2)
    v_y = p_y - x
    y += v_y * h

    Pdot_x, Pdot_y = [get_Pdot_x(x, y, p_x, p_y),get_Pdot_y(x, y, p_x, p_y)]
    p_x += Pdot_x * h
    p_y += Pdot_y * h
    return x, y, p_x, p_y


@jit
def verlet_step(h, x, y, p_x, p_y):
    """takes a half step, then another half step in the symplectic Verlet algorithm"""
    half_h = h / 2
    denominator = 1.0 / (1 + half_h ** 2)

    v_x = p_x + y
    x = (x + half_h * (v_x + p_y * half_h)) * denominator
    v_y = p_y - x
    y += v_y * half_h

    Pdot_x, Pdot_y = [get_Pdot_x(x, y, p_x, p_y), get_Pdot_y(x,y,p_x,p_y)]
    p_x = (p_x + (2.0 * Pdot_x + (Pdot_y * 2 + p_x) * half_h) * half_h) * denominator
    Pdot_y2 = get_Pdot_y(x, y, p_x, p_y)
    p_y += (Pdot_y * Pdot_y2) * half_h

    v_x = p_x + y
    v_y = p_y - x
    x += v_x * half_h
    y += v_y * half_h
    return x, y, p_x, p_y


@jit
def relative_error(vec1, vec2):
    x1, y1 = vec1
    x2, y2 = vec2
    return sqrt(((x2 - x1) ** 2 + (y2 - y1) ** 2) / (x2 ** 2 + y2 ** 2))


@jit
def symplectic(x0, y0, p0_x, p0_y, max_iter=1000, target=planet(celestials.MOON)):
    """
    runs symplectic adaptive euler-verlet algorithm
    All values are with nondimensionalized units
    """
    h = h_default
    hmin = h_min
    t = 0  # total elapsed time
    x, y, p_x, p_y = [x0, y0, p0_x, p0_y]

    path_storage = []
    path_storage.append([x, y, p_x, p_y, h])
    smallest_distance = 1e6
    Dv = 1e10
    count = 0
    orbital_radius_lower_bound, orbital_radius_upper_bound = target.get_orbital_bounds()
    print(orbital_radius_upper_bound)
    earth = planet(celestials.EARTH)
    for i in range(max_iter):

        x_euler, y_euler, p_euler_x, p_euler_y = euler_step(h, x, y, p_x, p_y)
        x_verlet, y_verlet, p_verlet_x, p_verlet_y = verlet_step(h, x, y, p_x, p_y)
        err = relative_error([x_euler, y_euler], [x_verlet, y_verlet])

        if err < tol or h <= hmin:
            x = x_verlet
            y = y_verlet
            p_x = p_verlet_x
            p_y = p_verlet_y

            t += h
            h = max(hmin, h * max(0.1, 0.8 * sqrt(tol / err)))
            # TODO: explain this with /HH's new comments. 0.8 is chosen empirically
            # old explanation below:
            """Accept the step only if the weighted error is no more than the
            tolerance tol.  Estimate an h that will yield an error of tol on
            the next step and use 0.8 of this value to avoid failures."""

        else:
            # print(f"deny step {h},{err}")
            h = max(hmin, h / 2)
            continue

        """Are we nearly there yet? (calculate distance)"""
        target_distance_x = x - target.position_x
        target_distance_y = y - target.position_y
        target_distance = sqrt(target_distance_x ** 2 + target_distance_y ** 2)
        smallest_distance = min(smallest_distance, target_distance)

        """For real though, are we there yet? (did we actually hit?)"""
        if (
            smallest_distance >= orbital_radius_lower_bound
            and smallest_distance <= orbital_radius_upper_bound
        ):
            """ we are in orbit range"""
            # current velocity vector
            v_x = p_x + y
            v_y = p_y - x

            """
            We adjust our velocity so the spacecraft enters a closed circular orbit.
            We treat target_distance as a vector from spacecraft to target
            """

            # project velocity vector onto radial direction unit-vector. This is what we
            # want to subtract from the velocity vector to obtain the tangental component (closed circular orbit)
            v_radial = (
                v_x * target_distance_x + v_y * target_distance_y
            ) / target_distance

            # phi is the angle of the radial vector
            cos_phi = target_distance_x / target_distance
            sin_phi = target_distance_y / target_distance
            # project radial velocity component to x and y axes.
            v_x = v_x - v_radial * cos_phi
            v_y = v_y - v_radial * sin_phi
            v_magnitude = sqrt(v_x ** 2 + v_y ** 2)

            # Delta-V for the maneuver
            Dv = sqrt(
                v_radial ** 2 + (v_magnitude - target.orbital_velocity_nondim) ** 2
            )

        path_storage.append([x, y, p_x, p_y, h])

        """check if we somehow accidentally struck the earth (whoops)"""

        earth_distance = sqrt((x - earth.position_x) ** 2 + (y - earth.position_y) ** 2)

        # not necessarily a crash, but we don't want paths that take us to such risky territories
        critical_distance = earth.get_critical_bounds()
        if earth_distance < critical_distance:
            print("Anga crashed into the earth!")
            return Dv, path_storage

    # import io
    # with open("tests/testsim.log", "w") as file:
    # file.writelines(str(path_storage))
    print("smallest distance =", smallest_distance)
    return Dv, path_storage
