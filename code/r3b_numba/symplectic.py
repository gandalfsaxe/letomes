"""
Reduced 3-Body Problem Solver Module
====================================
A collection of various numerical solvers for the reduced 3-body problem consisting of two larger masses (Earth, Moon) and one smaller moving in their gravitational field (a satellite). The solution assumes Earth-Moon center of mass as origin and a cartesian x-y coordinate system rotating with the lines connecting the Earth and Moon (non-inertial frame accounted for in the equations of motion).

Functions:
    euler: Solves by Euler method explicitly, implicitly or symplectically.

We assume TODO: FILL OUT HERE!

"""

from math import pi, sqrt

import numpy as np
from numba import jit

from orbsim.constants import (
    ORBITAL_TOLERANCE,
    day,
    earth_position_x,
    earth_radius,
    k,
    llo_radius,
    llo_velocity,
    lunar_position_x,
    unit_length,
    unit_velocity,
)


### TODO: DELETE SOON!!!
@jit
def F(x, y):
    denominator_1 = ((x + k) ** 2 + y ** 2) * sqrt((x + k) ** 2 + y ** 2)
    denominator_2 = ((1 - k - x) ** 2 + y ** 2) * sqrt((1 - k - x) ** 2 + y ** 2)
    Fx = -((1 - k) * (x + k)) / denominator_1 + k * (1 - k - x) / denominator_2
    Fy = -(1 - k) * y / denominator_1 - k * y / denominator_2
    return Fx, Fy


@jit
def explicit_euler_step(h, x, y, p_x, p_y):
    """
    Unused function, left here mostly to show the difference between explicit and
    symplectic integrators
    """
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


@jit
def explicit_euler_step(h, x, y, p_x, p_y):
    """
    Unused function, left here mostly to show the difference between explicit and
    symplectic integrators
    """
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


@jit
def symplectic_euler_step(h, x, y, p_x, p_y):
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
def symplectic_euler_step1(h, x, y, p_x, p_y):
    # Step 1
    pdot_x = get_pdot_x(x, y, p_y)
    p_x = (p_x + (pdot_x + Fy * h) * h) / (1.0 + h * h)
    pdot_y = get_pdot_y(x, y, p_x)
    p_y = p_y + pdot_y * h
    # Step 2
    v_x = get_v_x(y, p_x)
    v_y = get_v_y(x, p_y)
    x = x + v_x * h
    y = y + v_y * h
    return x, y, p_x, p_y


@jit
def symplectic_euler_step2(h, x, y, p_x, p_y):
    # Step 1
    pdot_x = get_pdot_x(x, y, p_y)
    pdot_y = get_pdot_y(x, y, p_x)
    p_x = p_x + pdot_x * h
    p_y = p_y + pdot_y * h
    # Step 2
    v_x = get_v_x(y, p_x)
    x = (x + (v_x + p_y * h) * h) / (1.0 + h * h)
    v_y = get_v_y(x, p_y)
    y = y + v_y * h
    return x, y, p_x, p_y


# @jit
# def symplectic_euler_step(h, x, y, p_x, p_y):
#     # Step 3
#     pdot_x = get_pdot_x(x, y, p_y)
#     pdot_y = get_pdot_y(x, y, p_x)
#     p_x = p_x + pdot_x * h
#     p_y = p_y + pdot_y * h
#     # Step 1
#     v_x = get_v_x(y, p_x)
#     x = (x + (v_x + p_y * h) * h) / (1.0 + h ** 2)
#     # Step 2
#     v_y = get_v_y(x, p_y)
#     y = y + v_y * h

#     return x, y, p_x, p_y


@jit
def symplectic_verlet_step(h, x, y, p_x, p_y):
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
    )  # TODO: mixed, that correct? Derive theory
    # Step 3
    v_x = get_v_x(y, p_x)
    v_y = get_v_y(x, p_y)
    x += v_x * hh
    y += v_y * hh

    return x, y, p_x, p_y


@jit  # ('void(int64, float64, float64, float64, float64, float64, float64, float64[:], float64[:], float64[:], float64[:])')
def symplectic(
    n, duration, x0, y0, p0_x, p0_y, xs, ys, p_xs, p_ys, step_errors, h_list, info
):

    # Initialize initial conditions
    h = 1e-6
    h_min = 1e-10
    tol = 1e-9
    max_steps = duration
    x = x0
    y = y0
    p_x = p0_x
    p_y = p0_y
    step_error = 1e-15
    status = 1
    target_dist = 1
    target = 1
    target_pos_x = lunar_position_x
    # target = 2; target_pos_x = L1_position_x
    target_pos_y = 0

    # Time reset
    t = 0
    for i in range(n):

        # Store position
        xs[i] = x
        ys[i] = y
        p_xs[i] = p_x
        p_ys[i] = p_y
        step_errors[i] = step_error
        h_list[i] = h

        # Integrate time period
        dt = duration * (i + 1) / n
        count = 0
        while t < dt:
            # Safety on iterations
            count += 1
            if count > 10000000:
                count = 0
                h_min = 2 * h_min

            # Adaptive symplectic euler/midpoint
            x1, y1, p1_x, p1_y = symplectic_euler_step(h, x, y, p_x, p_y)
            x2, y2, p2_x, p2_y = symplectic_verlet_step(h, x, y, p_x, p_y)

            # Relative local error of step
            step_error = sqrt(
                (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1) / (x2 * x2 + y2 * y2)
            )

            # Accept the step only if the weighted error is no more than the
            # tolerance tol.  Estimate an h that will yield an error of tol on
            # the next step and use 0.8 of this value to avoid failures.
            if step_error < tol or h <= h_min:

                # Accept step
                x = x2
                y = y2
                p_x = p2_x
                p_y = p2_y

                # Forward time by step
                t = t + h
                h = max(h_min, h * max(0.1, 0.8 * sqrt(tol / step_error)))

            else:
                # No accept, reduce h to half
                h = max(h_min, 0.5 * h)

            # How close are we to the moon?
            rx = x - target_pos_x
            ry = y - target_pos_y
            r = sqrt(rx * rx + ry * ry)
            target_dist = min(target_dist, r)

            # Check if we hit the target
            if status == 1:
                if target == 1:
                    r_low = (llo_radius - ORBITAL_TOLERANCE) / unit_length
                    r_high = (llo_radius + ORBITAL_TOLERANCE) / unit_length
                else:
                    r_low = 0
                    r_high = ORBITAL_TOLERANCE / unit_length

                if r > r_low and r < r_high:

                    # Current velocity
                    v_x = p_x + y
                    v_y = p_y - x

                    if target == 1:

                        # Project velocity onto radius vector and subtract
                        # so velocity vector is along orbit
                        vr = (v_x * rx + v_y * ry) / r
                        v_x = v_x - vr * rx / r
                        v_y = v_y - vr * ry / r

                        # Now adjust velocity to lunar orbit velocity
                        vt = sqrt(v_x * v_x + v_y * v_y)
                        p_x = (llo_velocity / unit_velocity) * v_x / vt - y
                        p_y = (llo_velocity / unit_velocity) * v_y / vt + x

                        # Total velocity change
                        dv = sqrt(
                            vr * vr
                            + (vt - llo_velocity / unit_velocity)
                            * (vt - llo_velocity / unit_velocity)
                        )
                    else:
                        dv = sqrt(v_x * v_x + v_y * v_y)

                    # Store info
                    info[0] = dv
                    info[1] = t

                    # Finish?
                    status = -10000 + dv
                    if n == 1:
                        return status

            # Check if we hit the earth
            r = (x - earth_position_x) * (x - earth_position_x) + y * y
            r_high = earth_radius / unit_length
            if r < r_high * r_high:
                return 100  # Hit earth surface

    if status >= 0:
        status = target_dist

    return status
