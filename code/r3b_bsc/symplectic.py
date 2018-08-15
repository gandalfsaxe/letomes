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

from orbsim import DAY, EARTH_RADIUS
from orbsim.r3b_2d import (
    ORBITAL_TOLERANCE,
    EARTH_POSITION_X,
    k,
    LLO_RADIUS,
    LLO_VELOCITY,
    LUNAR_POSITION_X,
    UNIT_LENGTH,
    UNIT_VELOCITY,
    h_DEFAULT,
    h_MIN_DEFAULT,
    STEP_ERROR_TOLERANCE,
)
from orbsim.r3b_2d.analyticals import get_pdot_x, get_pdot_y, get_v_x, get_v_y
from orbsim.r3b_2d.integrators import euler_step_symplectic, verlet_step_symplectic


@jit
def symplectic(
    n, duration, x, y, p_x, p_y, xs, ys, p_xs, p_ys, step_errors, h_list, info
):
    # Initialize values
    h = h_DEFAULT
    h_min = h_MIN_DEFAULT
    # STEP_ERROR_TOLERANCE = STEP_ERROR_TOLERANCE

    # max_steps = duration
    step_error = 1e-15
    status = 1
    target_dist = 1
    target = 1
    target_pos_x = LUNAR_POSITION_X
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
            x1, y1, p1_x, p1_y = euler_step_symplectic(h, x, y, p_x, p_y)
            x2, y2, p2_x, p2_y = verlet_step_symplectic(h, x, y, p_x, p_y)

            # Relative local error of step
            step_error = sqrt(
                (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1) / (x2 * x2 + y2 * y2)
            )

            # Accept the step only if the weighted error is no more than the
            # tolerance STEP_ERROR_TOLERANCE. Estimate an h that will yield an error of STEP_ERROR_TOLERANCE on
            # the next step and use 0.8 of this value to avoid failures.
            if step_error < STEP_ERROR_TOLERANCE or h <= h_min:

                # Accept step
                x = x2
                y = y2
                p_x = p2_x
                p_y = p2_y

                # Forward time by step
                t = t + h
                h = max(
                    h_min, h * max(0.1, 0.8 * sqrt(STEP_ERROR_TOLERANCE / step_error))
                )

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
                    r_low = (LLO_RADIUS - ORBITAL_TOLERANCE) / UNIT_LENGTH
                    r_high = (LLO_RADIUS + ORBITAL_TOLERANCE) / UNIT_LENGTH
                else:
                    r_low = 0
                    r_high = ORBITAL_TOLERANCE / UNIT_LENGTH

                if r > r_low and r < r_high:

                    # Current velocity
                    v_x = p_x + y
                    v_y = p_y - x

                    if target == 1:

                        # Project velocity onto radius vector and subtract
                        # so velocity vector is along orbit
                        vr = (v_x * rx + v_y * ry) / r  ## FIXME: Check if vr is correct
                        v_x = v_x - vr * rx / r
                        v_y = v_y - vr * ry / r

                        # Now adjust velocity to lunar orbit velocity
                        vt = sqrt(v_x * v_x + v_y * v_y)
                        p_x = (LLO_VELOCITY / UNIT_VELOCITY) * v_x / vt - y
                        p_y = (LLO_VELOCITY / UNIT_VELOCITY) * v_y / vt + x

                        # Total velocity change
                        dv = sqrt(
                            vr * vr
                            + (vt - LLO_VELOCITY / UNIT_VELOCITY)
                            * (vt - LLO_VELOCITY / UNIT_VELOCITY)
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
            r = (x - EARTH_POSITION_X) * (x - EARTH_POSITION_X) + y * y  # FIXME: sqrt?
            r_high = EARTH_RADIUS / UNIT_LENGTH
            if r < r_high * r_high:
                return 100  # Hit earth surface

    if status >= 0:
        status = target_dist

    return status
