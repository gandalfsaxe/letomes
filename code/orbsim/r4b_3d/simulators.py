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

from orbsim.r4b_3d.analyticals import (
    UNIT_TIME,
    get_B_phi,
    get_B_R,
    get_B_theta,
    get_leo_position_and_velocity,
)
from orbsim.r4b_3d.ephemerides import get_ephemerides, get_ephemerides_on_date
from orbsim.r4b_3d.integrators import euler_step_symplectic
from orbsim.r4b_3d.logging import logging_setup

# from numba import njit


# logging_setup()

logger = logging.getLogger()


def simulate(psi=(0, None), max_year="2020", max_duration=3, max_iter=int(10)):
    """Simple simulator that will run a LEO until duration or max_iter is reached.

    Keyword Arguments:
        psi {list} -- Initial conditions: [day] (default: {[0]})
        max_duration {int} -- Max duration of simulation (in years) (default: {3})
        max_iter {int} -- Max iterations of simulation (default: {1e7})

    Returns:
        [type] -- [description]
    """
    BODIES = {0: "sun", 1: "earth", 2: "mars"}

    logging.info("Starting simple simulation.")

    day = psi[0]

    # Read ephemerides
    logging.debug("Getting ephemerides tables")
    ephemerides = get_ephemerides(end_year=max_year)

    initial_eph = get_ephemerides_on_date(ephemerides, day)

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
    h = 1 / UNIT_TIME

    q_p_list = []

    while i < max_iter:

        eph_on_date = get_ephemerides_on_date(ephemerides, day)

        q_p = euler_step_symplectic(eph_on_date, h, R, theta, phi, B_R, B_theta, B_phi)

        q_p_list.append(q_p)

        i += 1

    return None


if __name__ == "__main__":
    simulate()
