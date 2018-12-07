"""
Repeatedly run single integration steps for some initial conditions until some stopping
conditions.
"""

import logging
import time
from decimal import Decimal
import numpy as np

from orbsim.r4b_3d import UNIT_TIME
from orbsim.r4b_3d.ephemerides import (
    get_coordinates_on_day_rad,
    get_ephemerides,
    get_ephemerides_on_day,
)

# from ctypes import cdll
from ctypes import *

cudasim = cdll.LoadLibrary("./libcudasim.so")

from math import pi
pi8 = pi / 8
pi4 = pi / 4
pi2 = pi / 2
tau = 2 * pi

#from orbsim.r4b_3d.integrators import euler_step_symplectic

def simulate(
    psi,
    max_year="2039",
    h=1 / UNIT_TIME,
    max_duration=1 * 3600 * 24 / UNIT_TIME,
    max_iter=int(1e6),
    number_of_paths=int(1),
    fan_delta=0.1,
    coordinate_no=int(0)
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
    t0 = time.time()
    max_iter = int(max_iter)

    # Unpack psi
    t = psi[0]
    Q = psi[1]
    B = psi[2]
    # burn = psi[3]

    day = t * UNIT_TIME / (3600 * 24)

    # Read ephemerides
    logging.debug("Getting ephemerides tables")
    ephemerides = get_ephemerides(max_year=max_year)
    earth = np.array(ephemerides['earth'])
    mars = np.array(ephemerides['mars'])

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
        f", in-sim time {format_time(t, time_unit='years')} / "
        f"{format_time(max_duration, time_unit='years')}"
        f"   (out-of-sim elapsed time: {format_time(sim_time)})"
    )


    """
    make list of all paths to integrate
    """
    successes = np.zeros(number_of_paths, dtype=bool)
    scores = np.zeros(number_of_paths)
    cudasim.simulate.restype = None
    cudasim.simulate.argtypes = [
        c_int,
        c_double,
        c_int,
        c_double,
        c_double,
        c_int,
        c_double,
        POINTER(c_double),
        POINTER(c_double),
        c_int,
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_bool),
        POINTER(c_double),
    ]

    Q = np.asarray(Q)
    B = np.asarray(B)
    earth_R = earth[:,3].astype(np.float64)
    earth_theta = earth[:,4].astype(np.float64) * pi / 180
    earth_phi = earth[:,5].astype(np.float64) * pi / 180
    mars_R = mars[:,3].astype(np.float64)
    mars_theta = mars[:,4].astype(np.float64) * pi / 180
    mars_phi = mars[:,5].astype(np.float64) * pi / 180
    Q_ctype = Q.ctypes.data_as(POINTER(c_double))
    B_ctype = B.ctypes.data_as(POINTER(c_double))
    earth_R_ctype = earth_R.ctypes.data_as(POINTER(c_double))
    earth_theta_ctype = earth_theta.ctypes.data_as(POINTER(c_double))
    earth_phi_ctype = earth_phi.ctypes.data_as(POINTER(c_double))
    mars_R_ctype = mars_R.ctypes.data_as(POINTER(c_double))
    mars_theta_ctype = mars_theta.ctypes.data_as(POINTER(c_double))
    mars_phi_ctype = mars_phi.ctypes.data_as(POINTER(c_double))
    success_ctype = successes.ctypes.data_as(POINTER(c_bool))
    score_ctype = scores.ctypes.data_as(POINTER(c_double))
    cudasim.simulate(
        number_of_paths,
        fan_delta,
        coordinate_no,
        h,
        max_duration,
        int(max_iter),
        t,
        Q_ctype,
        B_ctype,
        int(earth_R.size),
        earth_R_ctype,
        earth_theta_ctype,
        earth_phi_ctype,
        mars_R_ctype,
        mars_theta_ctype,
        mars_phi_ctype,
        success_ctype,
        score_ctype,
    )

    """
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

    """
    t += h;
    t_s = t * UNIT_TIME  # final in-sim time in seconds
    tf = time.time()
    T = tf - t0  # final out-of-sim time in seconds

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


# if __name__ == "__main__":
#     simulate()
