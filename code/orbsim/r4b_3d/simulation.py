"""
Repeatedly run single integration steps for some initial conditions until some stopping
conditions.

1. `analyticals.py`: set up the equations of motion.

2. `integrators.py`: discretize the equations of motion and defines a single time step of the
    chosen numerical algorithm.

3. `simulation.py`: run the single steps from `integrators.py` repeatedly for some initial
    conditions and stopping conditions.
"""

import logging
import time
from decimal import Decimal

import numpy as np

from orbsim.r4b_3d import UNIT_LENGTH, UNIT_TIME, UNIT_VELOCITY
from orbsim.r4b_3d.ephemerides import (
    get_coordinates_on_day_rad,
    get_ephemerides,
    get_ephemerides_on_day,
)
from orbsim.r4b_3d.integrators import euler_step_symplectic

from orbsim.r4b_3d.equations_of_motion import (
    get_Rdot,
    get_thetadot,
    get_phidot,
    get_B_R,
    get_B_theta,
    get_B_phi,
)

from orbsim.r4b_3d.coordinate_system import (
    get_speed_cartesian,
    get_speed_spherical,
    get_velocity_cartesian_from_spherical,
    get_velocity_spherical_from_cartesian,
    get_position_cartesian_from_spherical,
)


def simulate(
    psi,
    max_year="2039",
    h=1 / UNIT_TIME,
    max_duration=1 * 3600 * 24 / UNIT_TIME,
    max_iter=int(1e6),
):
    """Simple simulator that will run a LEO until duration or max_iter is reached.

    Keyword Arguments:
        psi {tuple} -- Initial conditions: (day, Q0, B0, burn)
        max_year {string} -- Max year for ephemerides table (default: "2020")
        h {float} -- Initial time step size (default: 1/UNIT_LENGTH = 1 second in years)
        max_duration {int} -- Max duration of simulation (in years) (default: {1 day})
        max_iter {int} -- Max number of iterations of simulation (default: {1e6})
                          (1e6 iterations corresponds to ~11 days with h = 1 s)

    Returns:
        [type] -- [description]
    """
    logging.info("STARTING: Simple simulation.")
    t_start = time.time()
    max_iter = int(max_iter)

    # Unpack psi
    day = psi[0]
    Q = psi[1]
    B = psi[2]
    delta_v0 = psi[3]

    t = day * 3600 * 24 / UNIT_TIME
    t0 = t

    # Read ephemerides
    logging.debug("Getting ephemerides tables")
    ephemerides = get_ephemerides(max_year=max_year)

    # Apply initial burn if delta_v input is provided
    if delta_v0:
        B = apply_delta_v(Q, B, delta_v0)

    # Unpack initial position (Q) and momenta (B)
    R, theta, phi = Q
    B_R, B_theta, B_phi = B

    logging.info(f"Initial coordinates: Q = {B} (R, theta, phi)")
    logging.info(f"Initial momenta: B = {B} (B_R, B_theta, B_phi")

    logging.info(
        f"Starting simulation at time {t} ({day} days) with step size h = {h} "
        f"({h*UNIT_TIME} s)"
        f", max {max_iter} iterations and max {max_duration*UNIT_TIME/3600/24} days"
    )

    # List initialization
    i = 0

    ts = []
    days = []
    Qs = []
    Bs = []
    q_p_list = []
    eph_body_coords = []

    # Run iteration 0 manually
    ts.append(t)
    days.append(day)
    Qs.append([R, theta, phi])
    Bs.append([B_R, B_theta, B_phi])
    q_p_list.append((Qs[0], Bs[0]))
    t1 = time.time()
    sim_time = t1 - t_start
    logging.info(
        f"Iteration {str(i).rjust(len(str(max_iter)))} / {max_iter}"
        f", in-sim time {format_time(t, time_unit='years')} / "
        f"{format_time(max_duration, time_unit='years')}"
        f"   (out-of-sim elapsed time: {format_time(sim_time)})"
    )

    # Iteration loop
    while True:
        i += 1
        t += h
        day = t * UNIT_TIME / (3600 * 24)

        eph_on_day = get_ephemerides_on_day(ephemerides, day)
        eph_coords = get_coordinates_on_day_rad(eph_on_day)

        sun = [coord[0] for coord in eph_coords]
        earth = [coord[1] for coord in eph_coords]
        mars = [coord[2] for coord in eph_coords]

        eph_body.coords.append([sun, earth, mars])

        Q, B = euler_step_symplectic(h, Q, B, eph_coords)

        ts.append(t)
        days.append(day)
        Qs.append(Q)
        Bs.append(B)
        q_p_list.append((Q, B))

        # Log status every 1000 iterations.
        if i % 1000 == 0:
            t1 = time.time()
            sim_time = t1 - t_start

            # if i > 10 ^ 4:
            #     h = 60 / UNIT_TIME
            #     logging.info(f"At iteration {i}, h now set to {h}")

            # if i > 10 ^ 5:
            #     h = 3600 / UNIT_TIME
            #     logging.info(f"At iteration {i}, h now set to {h}")

            # if i > 10 ^ 6:
            #     h = 3600 * 12 / UNIT_TIME
            #     logging.info(f"At iteration {i}, h now set to {h}")

            logging.info(
                f"Iteration {str(i).rjust(len(str(max_iter)))} / {max_iter}"
                f", in-sim time {format_time(t, time_unit='years')} / "
                f"{format_time(max_duration, time_unit='years')}"
                f"   (out-of-sim elapsed time: {format_time(sim_time)})"
            )

        # Stop simulation of max duration reached
        if (t - t0) >= max_duration:
            logging.info(
                f"STOP: Max time of {max_duration:.6f} "
                f"({format_time(max_duration, time_unit='years')}) "
                f"reached at t = {t:.6f} ({format_time(t, time_unit='years')})"
                f" at iteration: {i}/{max_iter} ~ {i/max_iter*100:.3f} %"
            )
            break

        # Stop simulation of max iterations reached
        if i >= max_iter:
            logging.info(
                f"STOP: Max iter of {max_iter} reached (i={i}) "
                f"at t = {format_time(t, time_unit='years')}/"
                f"{format_time(max_duration, time_unit='years')} ~ "
                f"{t/max_duration:.3f} %)"
            )
            break

        # Check for body collision
        x = 2

    t_s = (t - t0) * UNIT_TIME  # final in-sim time in seconds
    t_end = time.time()
    T = t_end - t_start  # final out-of-sim time in seconds

    # Post simulator run logging
    logging.info(
        f"SIMULATOR PERFORMANCE: Sim/Real time ratio:    "
        f"{Decimal(t_s / T):.2E} ({(t_s / T):.2f})"
    )
    logging.info(
        f"SIMULATOR PERFORMANCE: 1 second can simulate:  "
        f"{format_time(t_s / T)} (DDD:HH:MM:SS)"
    )
    logging.info(
        f"SIMULATOR PERFORMANCE: Time to simulate 1 day: "
        f"{format_time(T / t_s * 3600 * 24)} (DDD:HH:MM:SS)"
    )
    logging.info(
        f"TIME ELAPSED: In-sim time duration:     {format_time(t,time_unit='years')} "
        f"(DDD:HH:MM:SS)"
    )
    logging.info(
        f"TIME ELAPSED: Out-of-sim time duration: {format_time(T)} (DDD:HH:MM:SS)"
    )

    return (ts, Qs, Bs, (t, i), ephemerides)


def format_time(time_value, time_unit="seconds"):
    """Format time from a single unit (by default seconds) to a DDD:HH:MM:SS string

    Arguments:
        time {[float]} -- [Time value in some unit]

    Keyword Arguments:
        time_unit {str} -- [Time unit] (default: {"seconds"})

    Raises:
        ValueError -- [Unsupported input time unit]

    Returns:
        [str] -- [String of time formatted as DDD:HH:MM:SS]
    """

    if time_unit == "years":
        time_value = time_value * UNIT_TIME
    elif time_unit == "seconds":
        pass
    else:
        raise ValueError("Input time must be either 'years' or 'seconds' (default)")

    days = int(time_value // (3600 * 24))
    time_value %= 3600 * 24
    hours = int(time_value // 3600)
    time_value %= 3600
    minutes = int(time_value // 60)
    time_value %= 60
    seconds = time_value
    text = f"{days:0>3d}:{hours:0>2d}:{minutes:0>2d}:{seconds:0>5.2f}"

    return text


def apply_delta_v(Q, B, delta_v):
    """Apply an engine delta-v along velocity vector axis of delta-v"""

    # Unpack velocity and speed in cartesian coordinates
    R, theta, phi = Q
    B_R, B_theta, B_phi = B

    Rdot = get_Rdot(B_R)
    thetadot = get_thetadot(R, B_theta)
    phidot = get_phidot(R, theta, B_phi)

    Rdot *= UNIT_VELOCITY
    thetadot /= UNIT_TIME
    phidot /= UNIT_TIME
    R *= UNIT_LENGTH

    v_speed_spherical = get_speed_spherical(R, theta, Rdot, thetadot, phidot)

    v = get_velocity_cartesian_from_spherical([R, theta, phi], [Rdot, thetadot, phidot])
    v_speed = get_speed_cartesian(*v)

    logging.debug(
        f"Speed before burn (from spherical coords): {v_speed_spherical} km/s"
    )
    logging.info(f"Speed before burn: {v_speed} km/s")

    # Apply burn
    v_unit = v / np.linalg.norm(v)

    v2 = v + v_unit * delta_v

    v_speed2 = get_speed_cartesian(*v2)

    logging.info(f"Burn delta-v: {delta_v} km/s")
    logging.info(f"Speed after burn: {v_speed2} km/s")

    # Convert cartesian speed post-burn back into B
    pos = get_position_cartesian_from_spherical(R, theta, phi)
    v_postburn_spherical = get_velocity_spherical_from_cartesian(list(pos), v2)

    Rdot2, thetadot2, phidot2 = v_postburn_spherical
    R /= UNIT_LENGTH

    B_R2 = get_B_R(Rdot2 / UNIT_VELOCITY)
    B_theta2 = get_B_theta(R, thetadot2 * UNIT_TIME)
    B_phi2 = get_B_phi(R, theta, phidot2 * UNIT_TIME)

    B2 = [B_R2, B_theta2, B_phi2]

    logging.info(f"B before burn: {B}")
    logging.info(f"B after burn: {B}")

    return B2


# if __name__ == "__main__":
#     simulate()
