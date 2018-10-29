"""
Repeatedly run single integration steps for some initial conditions until some stopping
conditions.

1. `analyticals.py`: set up the equations of motion.

2. `integrators.py`: discretize the equations of motion and defines a single time step of the
    chosen numerical algorithm.

3. `simulators.py`: run the single steps from `integrators.py` repeatedly for some initial
    conditions and stopping conditions.
"""

# from typing import Callable, Iterable, Union, Optional, List

# import time

import logging
from pprint import pprint

from orbsim.r4b_3d import UNIT_TIME
from orbsim.r4b_3d.analyticals import (
    get_B_phi,
    get_B_R,
    get_B_theta,
    get_leo_position_and_velocity,
)
from orbsim.r4b_3d.ephemerides import get_ephemerides, get_ephemerides_on_day
from orbsim.r4b_3d.integrators import euler_step_symplectic

# from orbsim.r4b_3d.logging import logging_setup

# from numba import njit


# logging_setup()

# logger = logging.getLogger()


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

    max_iter = int(max_iter)
    day = psi[0]

    # Read ephemerides
    logging.debug("Getting ephemerides tables")
    ephemerides = get_ephemerides(end_year=max_year)

    # Initial spacecraft position and velocity (spherical)
    leo_position_spherical, leo_velocity_spherical = get_leo_position_and_velocity(
        ephemerides, day=day
    )

    # Initial position (q)
    R, theta, phi = leo_position_spherical

    # Initial momenta (p)
    Rdot, thetadot, phidot = leo_velocity_spherical
    B_R = get_B_R(Rdot)
    B_theta = get_B_theta(R, thetadot)
    B_phi = get_B_phi(R, theta, phidot)

    i = 0
    t = 0

    qs = []
    ps = []
    q_p_list = []

    logging.debug(
        f"Starting simulation with h = {h} ({h*UNIT_TIME} s)"
        f", max {max_iter} iterations and max {max_duration*UNIT_TIME/3600/24} days"
    )

    while True:
        eph_on_date = get_ephemerides_on_day(ephemerides, day)

        R, theta, phi, B_r, B_theta, B_phi = euler_step_symplectic(
            eph_on_date, h, R, theta, phi, B_R, B_theta, B_phi
        )

        q = [R, theta, phi]
        p = [B_r, B_theta, B_phi]
        qs.append(q)
        ps.append(p)
        q_p_list.append((q, p))

        i += 1
        t += h

        if i % 1000 == 0:
            logging.debug(
                f"Iteration {i} / {max_iter}"
                f", time {t*UNIT_TIME/3600:.2f} hours / "
                f"{max_duration*UNIT_TIME/3600:.2f} hours"
            )

        if i >= max_iter:
            logging.info(
                f"Max iter of {max_iter} reached (i={i}) "
                f"at t = {t:.6f} ({t*UNIT_TIME/3600/24:.2f}/"
                f"{max_duration*UNIT_TIME/3600/24:.2f} days ~ "
                f"{t/max_duration:.3f} %)"
            )
            break
        if t >= max_duration:
            logging.info(
                f"Max time of {max_duration:.6f} ({max_duration*UNIT_TIME/3600/24:.6f} "
                f"days) reached at t = {t:.6f} ({t*UNIT_TIME/3600/24:.6f} days)"
                f" at iteration: {i}/{max_iter} ~ {i/max_iter*100:.3f} %"
            )
            break

    # pprint(qs)

    return None


if __name__ == "__main__":
    simulate()
