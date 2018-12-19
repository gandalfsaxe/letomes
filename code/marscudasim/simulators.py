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
    t0 = time.time()
    max_iter = int(max_iter)

    # Unpack psi
    days = np.array(psi[0])
    ts = days * (3600 * 24) / UNIT_TIME
    Qs = np.array(psi[1])
    Bs = np.array(psi[2])
    nPaths = Qs.shape[0]

    # Read ephemerides
    logging.debug("Getting ephemerides tables")
    ephemerides = get_ephemerides(max_year=max_year)
    earth = np.array(ephemerides['earth'])
    mars = np.array(ephemerides['mars'])

    """
    make list of all paths to integrate
    """

    ts = np.asarray(ts)
    Rs = np.array(Qs[:,0])
    thetas = np.array(Qs[:,1])
    phis = np.array(Qs[:,2])
    B_Rs = np.array(Bs[:,0])
    B_thetas = np.array(Bs[:,1])
    B_phis = np.array(Bs[:,2])
    arives = np.zeros(nPaths)
    scores = np.zeros(nPaths)
    cudasim.simulate.restype = None
    cudasim.simulate.argtypes = [
        c_int,
        c_double,
        c_double,
        c_int,
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        c_int,
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
    ]

    earth_R = earth[:,3].astype(np.float64)
    earth_theta = earth[:,4].astype(np.float64) * pi / 180
    earth_phi = earth[:,5].astype(np.float64) * pi / 180
    mars_R = mars[:,3].astype(np.float64)
    mars_theta = mars[:,4].astype(np.float64) * pi / 180
    mars_phi = mars[:,5].astype(np.float64) * pi / 180

    ts_ctype = ts.ctypes.data_as(POINTER(c_double))
    Rs_ctype = Rs.ctypes.data_as(POINTER(c_double))
    thetas_ctype = thetas.ctypes.data_as(POINTER(c_double))
    phis_ctype = phis.ctypes.data_as(POINTER(c_double))
    B_Rs_ctype = B_Rs.ctypes.data_as(POINTER(c_double))
    B_thetas_ctype = B_thetas.ctypes.data_as(POINTER(c_double))
    B_phis_ctype = B_phis.ctypes.data_as(POINTER(c_double))

    earth_R_ctype = earth_R.ctypes.data_as(POINTER(c_double))
    earth_theta_ctype = earth_theta.ctypes.data_as(POINTER(c_double))
    earth_phi_ctype = earth_phi.ctypes.data_as(POINTER(c_double))
    mars_R_ctype = mars_R.ctypes.data_as(POINTER(c_double))
    mars_theta_ctype = mars_theta.ctypes.data_as(POINTER(c_double))
    mars_phi_ctype = mars_phi.ctypes.data_as(POINTER(c_double))
    arive_ctype = arives.ctypes.data_as(POINTER(c_double))
    score_ctype = scores.ctypes.data_as(POINTER(c_double))
    cudasim.simulate(
        nPaths,
        h,
        max_duration,
        int(max_iter),
        ts_ctype,
        Rs_ctype,
        thetas_ctype,
        phis_ctype,
        B_Rs_ctype,
        B_thetas_ctype,
        B_phis_ctype,
        int(earth_R.size),
        earth_R_ctype,
        earth_theta_ctype,
        earth_phi_ctype,
        mars_R_ctype,
        mars_theta_ctype,
        mars_phi_ctype,
        arive_ctype,
        score_ctype,
    )

    return arives, scores

def simulate_single(
    psi,
    max_year="2039",
    h=1 / UNIT_TIME,
    max_duration=1 * 3600 * 24 / UNIT_TIME,
    max_iter=int(1e6),
):
    logging.info("STARTING: Simple simulation.")
    t0 = time.time()
    max_iter = int(max_iter)

    # Unpack psi
    days = np.array(psi[0])
    ts = days * (3600 * 24) / UNIT_TIME
    Qs = np.array(psi[1])
    Bs = np.array(psi[2])
    nSteps = int(max_duration / (h - 1e-14))

    # Read ephemerides
    logging.debug("Getting ephemerides tables")
    ephemerides = get_ephemerides(max_year=max_year)

    earth = np.array(ephemerides['earth'])
    mars = np.array(ephemerides['mars'])
    ts = np.asarray(ts)
    Rs = np.array(Qs[:,0])
    thetas = np.array(Qs[:,1])
    phis = np.array(Qs[:,2])
    B_Rs = np.array(Bs[:,0])
    B_thetas = np.array(Bs[:,1])
    B_phis = np.array(Bs[:,2])
    ts_out = np.zeros(nSteps)
    Qs_out = np.zeros((nSteps, 3))
    #ts_out[:] = 0
    #Qs_out[:] = 0
    #ts_out = np.repeat(0.0, nSteps)
    #Qs_out = np.repeat(0.0, nSteps*3)
    #Qs_out.shape = (nSteps, 3)
    #print("nSteps=", nSteps, "size=", Qs_out.size)
    i_final = np.zeros(1, int)
    cudasim.simulate_cpu.restype = None
    cudasim.simulate_cpu.argtypes = [
        c_double,
        c_double,
        c_int,
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        c_int,
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_double),
        POINTER(c_int),
    ]

    earth_R = earth[:,3].astype(np.float64)
    earth_theta = earth[:,4].astype(np.float64) * pi / 180
    earth_phi = earth[:,5].astype(np.float64) * pi / 180
    mars_R = mars[:,3].astype(np.float64)
    mars_theta = mars[:,4].astype(np.float64) * pi / 180
    mars_phi = mars[:,5].astype(np.float64) * pi / 180

    ts_ctype = ts.ctypes.data_as(POINTER(c_double))
    Rs_ctype = Rs.ctypes.data_as(POINTER(c_double))
    thetas_ctype = thetas.ctypes.data_as(POINTER(c_double))
    phis_ctype = phis.ctypes.data_as(POINTER(c_double))
    B_Rs_ctype = B_Rs.ctypes.data_as(POINTER(c_double))
    B_thetas_ctype = B_thetas.ctypes.data_as(POINTER(c_double))
    B_phis_ctype = B_phis.ctypes.data_as(POINTER(c_double))

    earth_R_ctype = earth_R.ctypes.data_as(POINTER(c_double))
    earth_theta_ctype = earth_theta.ctypes.data_as(POINTER(c_double))
    earth_phi_ctype = earth_phi.ctypes.data_as(POINTER(c_double))
    mars_R_ctype = mars_R.ctypes.data_as(POINTER(c_double))
    mars_theta_ctype = mars_theta.ctypes.data_as(POINTER(c_double))
    mars_phi_ctype = mars_phi.ctypes.data_as(POINTER(c_double))
    ts_out_ctype = ts_out.ctypes.data_as(POINTER(c_double))
    Qs_out_ctype = Qs_out.ctypes.data_as(POINTER(c_double))
    i_final_ctype = i_final.ctypes.data_as(POINTER(c_int))
    cudasim.simulate_cpu(
        h,
        max_duration,
        int(max_iter),
        ts_ctype,
        Rs_ctype,
        thetas_ctype,
        phis_ctype,
        B_Rs_ctype,
        B_thetas_ctype,
        B_phis_ctype,
        int(earth_R.size),
        earth_R_ctype,
        earth_theta_ctype,
        earth_phi_ctype,
        mars_R_ctype,
        mars_theta_ctype,
        mars_phi_ctype,
        ts_out_ctype,
        Qs_out_ctype,
        i_final_ctype,
    )

    return ts_out, Qs_out, i_final

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
