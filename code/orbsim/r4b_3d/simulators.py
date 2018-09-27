# import time

from math import cos, sin, sqrt, acos, atan, pi

import numpy as np
from numba import njit

from orbsim.r4b_3d import (
    h_DEFAULT,
    h_MIN_DEFAULT,
    LEO_RADIUS_NONDIM,
    LEO_VELOCITY_NONDIM,
    UNIT_LENGTH,
    UNIT_TIME,
    UNIT_VELOCITY,
)
from orbsim.r4b_3d.analyticals import get_xyz, get_spherical, get_distance_xyz

from orbsim.r4b_3d.integrators import euler_step_symplectic

from orbsim.r4b_3d.ephemerides import get_ephemerides, get_ephemerides_on_date

# @njit
def simulate(
    R0,
    theta0,
    phi0,
    B_R0,
    B_theta0,
    B_phi0,
    score,
    success,
    duration=3 / UNIT_TIME,
    max_iter=10000,
):
    """
    Formerly symplectic()
    runs symplectic adaptive euler-verlet algorithm
    All values are with nondimensionalized units
    """
    success[0] = 0
    h = h_DEFAULT
    h_min = h_MIN_DEFAULT
    t = 0  # total elapsed time
    R, theta, phi, B_r, B_theta, B_phi = [R0, theta0, phi0, B_R0, B_theta0, B_phi0]

    path_storage = []
    path_storage.append([R, theta, phi, B_r, B_theta, B_phi, h, t])
    smallest_distance = 1e6
    Dv = None
    iteration_count = 0
    # print(orbital_radius_upper_bound)
    # earth = Planet(celestials.EARTH)
    # target_orbital_radius = LLO_RADIUS
    # target_orbital_velocity = LLO_VELOCITY
    # target_position_x = LUNAR_POSITION_X
    # target_position_y = 0
    # target_celestial_radius = LUNAR_RADIUS
    # target_celestial_mass = LUNAR_MASS
    # target_altitude = LUNAR_ALTITUDE
    # target_orbital_radius_nondim = target_orbital_radius / UNIT_LENGTH
    # target_orbital_velocity_nondim = target_orbital_velocity / UNIT_VELOCITY

    # earth_orbital_radius = LEO_RADIUS
    # earth_orbital_velocity = LEO_VELOCITY
    # earth_position_x = EARTH_POSITION_X
    # earth_position_y = 0
    # earth_celestial_radius = EARTH_RADIUS
    # earth_celestial_mass = EARTH_MASS
    # earth_altitude = EARTH_ALTITUDE
    # earth_orbital_radius_nondim = LEO_RADIUS_NONDIM
    # earth_orbital_velocity_nondim = LEO_VELOCITY_NONDIM

    # orbital_radius_lower_bound = (
    #     target_orbital_radius - ORBITAL_TOLERANCE
    # ) / UNIT_LENGTH
    # orbital_radius_upper_bound = (
    #     target_orbital_radius + ORBITAL_TOLERANCE
    # ) / UNIT_LENGTH
    while t < duration:
        if iteration_count > max_iter:
            # print("exceeded max iterations, stranded in space!")
            score[0] = smallest_distance
            return path_storage
        ephemerides_on_date = get_ephemerides_on_date(t / (24 * 3600))
        # earth_on_date = ephemerides_on_date["earth"]
        mars_on_date = ephemerides_on_date["mars"]

        R_euler, theta_euler, phi_euler, _, _, _ = euler_step_symplectic(
            ephemerides_on_date, h, R, theta, phi, B_r, B_theta, B_phi
        )

        x_euler, y_euler, z_euler = get_xyz(R_euler, theta_euler, phi_euler)

        x, y, z = x_euler, y_euler, z_euler

        # x_verlet, y_verlet, p_verlet_x, p_verlet_y = verlet_step_symplectic(
        #     h, x, y, p_x, p_y
        # )
        # err = relative_error([x_euler, y_euler], [x_verlet, y_verlet])

        # if err < STEP_ERROR_TOLERANCE or h <= h_min:
        #     iteration_count += 1
        #     x = x_verlet
        #     y = y_verlet
        #     p_x = p_verlet_x
        #     p_y = p_verlet_y

        #     t += h
        #     h = max(h_min, h * max(0.1, 0.8 * sqrt(STEP_ERROR_TOLERANCE / err)))
        #     # TODO: explain this with /HH's new comments. 0.8 is chosen empirically
        #     # old explanation below:
        #     """Accept the step only if the weighted error is no more than the
        #     tolerance tol.  Estimate an h that will yield an error of tol on
        #     the next step and use 0.8 of this value to avoid failures."""

        # else:
        #     # print(f"deny step {h},{err}")
        #     h = max(h_min, h / 2)
        #     continue

        """Are we nearly there yet? (calculate distance)"""
        target_distance = get_distance_xyz(
            x, y, z, mars_on_date["x"], mars_on_date["y"], mars_on_date["z"]
        )

        if target_distance > 1e9 / UNIT_LENGTH:
            # print("we are way too far away, stranded in space!")
            score[0] = smallest_distance
            return path_storage
        smallest_distance = min(smallest_distance, target_distance)

        # """For real though, are we there yet? (did we actually hit?)"""
        # if (
        #     smallest_distance >= orbital_radius_lower_bound
        #     and smallest_distance <= orbital_radius_upper_bound
        # ):
        #     """ SUCCESS! We are in orbit range"""
        #     # current velocity vector
        #     v_x = p_x + y
        #     v_y = p_y - x

        #     """
        #     We adjust our velocity so the spacecraft enters a closed circular orbit.
        #     We treat target_distance as a vector from spacecraft to target
        #     """

        #     # project velocity vector onto radial direction unit-vector. This is what we
        #     # want to subtract from the velocity vector to obtain the tangential
        #     # component (closed circular orbit)
        #     v_radial = (
        #         v_x * target_distance_x + v_y * target_distance_y
        #     ) / target_distance

        #     # phi is the angle of the radial vector
        #     cos_phi = target_distance_x / target_distance
        #     sin_phi = target_distance_y / target_distance
        #     # project radial velocity component to x and y axes.
        #     v_x = v_x - v_radial * cos_phi
        #     v_y = v_y - v_radial * sin_phi
        #     v_magnitude = sqrt(v_x ** 2 + v_y ** 2)

        #     # Delta-V for the maneuver
        #     Dv = sqrt(
        #         v_radial ** 2 + (v_magnitude - target_orbital_velocity_nondim) ** 2
        #     )
        #     path_storage.append([x, y, p_x, p_y, h, t])
        #     success[0] = 1
        #     score[0] = Dv
        #     return path_storage

        path_storage.append([R, theta, phi, B_r, B_theta, B_phi, t])

        # """check if we somehow accidentally struck the earth (whoops)"""

        # earth_distance = sqrt((x - earth_position_x) ** 2 + (y - earth_position_y) ** 2)

        # # not necessarily a crash, but we don't want paths that take us to such risky territories
        # critical_distance = (earth_celestial_radius / UNIT_LENGTH) ** 2
        # if earth_distance < critical_distance:
        #     # print("Anga crashed into the earth!")
        #     score[0] = smallest_distance
        #     return path_storage

    # import io
    # with open("tests/testsim.log", "w") as file:
    # file.writelines(str(path_storage))
    # print("smallest distance =", smallest_distance)
    score[0] = smallest_distance
    return path_storage


# @njit
def launch_sim(psi, duration=3, max_iter=1e7):
    """
    return: [Dv, [x, y, px, py, h]]
    launch (not really a launch since we start from LEO) a
    single rocket with a given set of hyperparameters, return the resulting path
    """
    t_day, burnDv = psi  # extract parameters from decision vector
    burnDv /= UNIT_VELOCITY
    duration /= UNIT_TIME

    # Read ephemerides
    ephemerides = get_ephemerides()

    day_zero_eph = ephemerides["earth"].iloc[0]

    earth_r0 = day_zero_eph["r"]
    earth_theta0 = day_zero_eph["theta"] * pi / 180
    earth_phi0 = day_zero_eph["phi"] * pi / 180
    # earth_x0 = day_zero_eph["x"]
    # earth_y0 = day_zero_eph["y"]
    # earth_z0 = day_zero_eph["z"]

    # Get initial position of earth
    earth_position_x, earth_position_y, earth_position_z = get_xyz(
        earth_r0, earth_theta0, earth_phi0
    )

    """define init params"""
    # position (where on earth do we start our burn)
    x0 = LEO_RADIUS_NONDIM  # geocentric
    y0 = 0  # geocentric
    z0 = 0  # geocentric
    x0 += earth_position_x  # heliocentric
    y0 += earth_position_y  # heliocentric
    z0 += earth_position_z  # heliocentric

    # how fast are we going when we start?
    earth_velocity_x = -6.282939073970666
    earth_velocity_y = -1.0714089257187907
    earth_velocity_z = -0.4643489045706851

    v_x0 = earth_velocity_x
    v_y0 = earth_velocity_y + LEO_VELOCITY_NONDIM
    v_z0 = earth_velocity_z

    # burn vector: At what angle do we launch outward, and how hard do we push?'
    # We choose fixed burn angle = 0, kept for R3B comparison purposes
    burnDv_x = 1
    burnDv_y = 0
    burnDv_z = 0

    # R, theta, phi and their velocities
    R0, theta0, phi0 = get_spherical(x0, y0, z0)
    R0dot, theta0dot, phi0dot = get_spherical(v_x0, v_y0, v_z0)

    # resultant momentum vector
    B_r0 = R0dot
    B_theta0 = R0 ** 2 * theta0dot
    B_phi0 = R0 ** 2 * sin(theta0) ** 2 * phi0dot

    """SIMULATE"""
    # print(f"running symplectic with [x0, y0, p0_x, p0_y]{[x0, y0, p0_x, p0_y]}")
    # starttime = time.time()
    score = [0.0]
    success = [0]
    path = simulate(
        R0,
        theta0,
        phi0,
        B_r0,
        B_theta0,
        B_phi0,
        score,
        success,
        duration=duration,
        max_iter=int(max_iter),
    )

    # return success[0], score[0], path
    if success[0] == 1:
        # print("SUCCESS")
        final_score = score[0] + burnDv
        # print("score = ", final_score)
    else:
        final_score = (1 + score[0]) * 10
        # print("score = ", final_score)

    return final_score, path


if __name__ == "__main__":
    launch_sim([0, 0])

