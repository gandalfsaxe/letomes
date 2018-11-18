"""
Repeatedly run single integration steps for some initial conditions until some stopping
conditions.

1. `analyticals.py`: set up the equations of motion.

2. `integrators.py`: discretize the equations of motion and defines a single time step of the
    chosen numerical algorithm.

3. `simulators.py`: run the single steps from `integrators.py` repeatedly for some initial
    conditions and stopping conditions.
"""

import logging
import time

from orbsim.r4b_3d import UNIT_TIME
from orbsim.r4b_3d.ephemerides import (
    get_coordinates_on_day_rad,
    get_ephemerides,
    get_ephemerides_on_day,
)
from orbsim.r4b_3d.equations_of_motion import get_B_phi, get_B_R, get_B_theta
from orbsim.r4b_3d.equations_of_physics import get_leo_position_and_velocity
from orbsim.r4b_3d.integrators import euler_step_symplectic


def simulate(
    psi=(0, None),
    max_year="2020",
    h=1 / UNIT_TIME,
    max_duration=1 * 3600 * 24 / UNIT_TIME,
    max_iter=int(1e6),
):
    """Simple simulator that will run a LEO until duration or max_iter is reached.

    Keyword Arguments:
        psi {list} -- Initial conditions: [day] (default: {[0]})
        max_year {string} -- Max year for ephemerides table (default: "2020")
        h {float} -- Initial time step size (default: 1/UNIT_LENGTH = 1 second in years)
        max_duration {int} -- Max duration of simulation (in years) (default: {1 day})
        max_iter {int} -- Max number of iterations of simulation (default: {1e6})
                          (1e6 iterations corresponds to ~11 days with h = 1 s)

    Returns:
        [type] -- [description]
    """
    logging.info("Starting simple simulation.")
    t0 = time.time()

    max_iter = int(max_iter)
    t = psi[0]
    day = t * UNIT_TIME / (3600 * 24)

    # Read ephemerides
    logging.debug("Getting ephemerides tables")
    ephemerides = get_ephemerides(end_year=max_year)

    # Initial spacecraft position and velocity (spherical)
    leo_position_spherical, leo_velocity_spherical = get_leo_position_and_velocity(
        day=day
    )

    # Initial position (q)
    R, theta, phi = leo_position_spherical
    Q = leo_position_spherical

    # Initial velocity
    Rdot, thetadot, phidot = leo_velocity_spherical

    # Initial momenta (p)
    B_R = get_B_R(Rdot)
    B_theta = get_B_theta(R, thetadot)
    B_phi = get_B_phi(R, theta, phidot)

    B = [B_R, B_theta, B_phi]

    logging.debug(
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

    # Run iteration 0 manually
    ts.append(t)
    days.append(day)
    Qs.append([R, theta, phi])
    Bs.append([B_R, B_theta, B_phi])
    q_p_list.append((Qs[0], Bs[0]))
    t1 = time.time()
    sim_time = t1 - t0
    logging.info(
        f"Iteration {str(i).rjust(len(str(max_iter)))} / {max_iter}"
        f", in-sim time {t*UNIT_TIME/3600:.2f} hours / "
        f"{max_duration*UNIT_TIME/3600:.2f} hours"
        f"   (out-of-sim elapsed time: {format_time(sim_time)})"
    )

    # Iteration loop
    while True:
        i += 1
        t += h
        day = t * UNIT_TIME / (3600 * 24)

        eph_on_day = get_ephemerides_on_day(ephemerides, day)
        eph_coords = get_coordinates_on_day_rad(eph_on_day)

        Q, B = euler_step_symplectic(h, Q, B, eph_coords)

        ts.append(t)
        days.append(day)
        Qs.append(Q)
        Bs.append(B)
        q_p_list.append((Q, B))

        # Log status every 1000 iterations.
        if i % 1000 == 0:
            t1 = time.time()
            sim_time = t1 - t0

            logging.info(
                f"Iteration {str(i).rjust(len(str(max_iter)))} / {max_iter}"
                f", in-sim time {format_time(t, time_unit='years')} / "
                f"{format_time(max_duration, time_unit='years')}"
                f"   (out-of-sim elapsed time: {format_time(sim_time)})"
            )

        # Stop simulation of max duration reached
        if t >= max_duration:
            logging.info(
                f"Max time of {max_duration:.6f} "
                f"({format_time(max_duration, time_unit='years')}) "
                f"reached at t = {t:.6f} ({format_time(t, time_unit='years')})"
                f" at iteration: {i}/{max_iter} ~ {i/max_iter*100:.3f} %"
            )
            break

        # Stop simulation of max iterations reached
        if i >= max_iter:
            logging.info(
                f"Max iter of {max_iter} reached (i={i}) "
                f"at t = {format_time(t, time_unit='years')}/"
                f"{format_time(max_duration, time_unit='years')} ~ "
                f"{t/max_duration:.3f} %)"
            )
            break

    tf = time.time()
    total_time = tf - t0
    logging.info(f"Simulation duration: {format_time(total_time)} (HH:MM:SS)")

    return (ts, Qs, Bs, (t, i), ephemerides)


def format_time(time_value, time_unit="seconds"):
    """Format time from a single unit (by default seconds) to a nice HH:MM:SS string

    Arguments:
        time {[float]} -- [Time value in some unit]

    Keyword Arguments:
        time_unit {str} -- [Time unit] (default: {"seconds"})

    Raises:
        ValueError -- [Unsupported input time unit]

    Returns:
        [str] -- [String of time formatted as HH:MM:SS]
    """

    if time_unit == "years":
        time_value = time_value * UNIT_TIME
    elif time_unit == "seconds":
        pass
    else:
        raise ValueError("Input time must be either 'years' or 'seconds' (default)")

    hours = int(time_value // 3600)
    time_value %= 3600
    minutes = int(time_value // 60)
    time_value %= 60
    seconds = time_value
    text = f"{hours:0>2d}:{minutes:0>2d}:{seconds:.2f}"

    return text


if __name__ == "__main__":
    simulate()
