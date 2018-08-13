import time
from math import sqrt

from numba import jit

from . import h_default, h_min, tol, unit_length, unit_time
from ..planets import celestials, Planet
from .analyticals import get_pdot_x, get_pdot_y, get_v_x, get_v_y


@jit
def euler_step_symplectic(h, x, y, p_x, p_y):
    """Takes a single time step of the symplectic Euler algorithm"""
    # Step 1
    v_x = get_v_x(y, p_x)
    x = (x + (v_x + p_y * h) * h) / (1.0 + h ** 2)
    # Step 2
    v_y = get_v_y(x, p_y)
    y = y + v_y * h
    # Step 3
    pdot_x = get_pdot_x(x, y, p_y)
    pdot_y = get_pdot_y(x, y, p_x)
    p_x = p_x + pdot_x * h
    p_y = p_y + pdot_y * h

    return x, y, p_x, p_y


@jit
def verlet_step_symplectic(h, x, y, p_x, p_y):
    """Takes a half step, then another half step in the symplectic Verlet algorithm"""
    hh = 0.5 * h
    denominator = 1.0 / (1.0 + hh ** 2)
    # Step 1
    v_x = get_v_x(y, p_x)
    x = (x + (v_x + p_y * hh) * hh) * denominator
    # Step 2
    v_y = get_v_y(x, p_y)
    y = y + v_y * hh
    # Step 2
    pdot_x = get_pdot_x(x, y, p_y)
    pdot_y = get_pdot_y(x, y, p_x)
    p_x = (p_x + (2.0 * pdot_x + (2 * pdot_y + p_x) * hh) * hh) * denominator
    p_y = (
        p_y + (pdot_y + get_pdot_y(x, y, p_x)) * hh
    )  # TODO: mixed, what's correct? Derive theory
    # Step 3
    v_x = get_v_x(y, p_x)
    v_y = get_v_y(x, p_y)
    x += v_x * hh
    y += v_y * hh

    return x, y, p_x, p_y


@jit
def relative_error(vec1, vec2):
    x1, y1 = vec1
    x2, y2 = vec2
    return sqrt(((x2 - x1) ** 2 + (y2 - y1) ** 2) / (x2 ** 2 + y2 ** 2))


@jit
def symplectic(
    x0,
    y0,
    p0_x,
    p0_y,
    duration=3 / unit_time,
    max_iter=1000,
    target=Planet(celestials.MOON),
):
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
    Dv = None
    iteration_count = 0
    orbital_radius_lower_bound, orbital_radius_upper_bound = target.get_orbital_bounds()
    # print(orbital_radius_upper_bound)
    earth = Planet(celestials.EARTH)
    while t < duration:
        iteration_count += 1
        if iteration_count > max_iter:
            print("exceeded max iterations, stranded in space!")
            return False, smallest_distance, path_storage

        x_euler, y_euler, p_euler_x, p_euler_y = euler_step_symplectic(
            h, x, y, p_x, p_y
        )
        x_verlet, y_verlet, p_verlet_x, p_verlet_y = verlet_step_symplectic(
            h, x, y, p_x, p_y
        )
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
        if target_distance > 1e9 / unit_length:
            print("we are way too far away, stranded in space!")
            return False, smallest_distance, path_storage
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
            break

        path_storage.append([x, y, p_x, p_y, h])

        """check if we somehow accidentally struck the earth (whoops)"""

        earth_distance = sqrt((x - earth.position_x) ** 2 + (y - earth.position_y) ** 2)

        # not necessarily a crash, but we don't want paths that take us to such risky territories
        critical_distance = earth.get_critical_bounds()
        if earth_distance < critical_distance:
            # print("Anga crashed into the earth!")
            return True, Dv, path_storage

    # import io
    # with open("tests/testsim.log", "w") as file:
    # file.writelines(str(path_storage))
    # print("smallest distance =", smallest_distance)
    print([x, y, p_x, p_y, h])
    return False, smallest_distance, path_storage


# region Unused integrators


@jit
def unused_explicit_euler_step(h, x, y, p_x, p_y):
    # Step 1 - get all time derivatives
    v_x = get_v_x(y, p_x)
    v_y = get_v_y(x, p_y)
    pdot_x = get_pdot_x(x, y, p_y)
    pdot_y = get_pdot_y(x, y, p_x)
    # Step 2 - linear extrapolation
    x = x + v_x * h
    y = y + v_y * h
    p_x = p_x + pdot_x * h
    p_y = p_y + pdot_y * h

    return x, y, p_x, p_y


# endregion
