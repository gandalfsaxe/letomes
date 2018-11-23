"""Run the R4B simulator"""

import logging
import pathlib
import sys

import matplotlib.pyplot as plt

from orbsim.r4b_3d import UNIT_TIME
from orbsim.r4b_3d.initial_conditions import (
    get_leo_position_and_velocity,
    get_circular_sun_orbit_position_and_velocity,
)
from orbsim.r4b_3d.logging import logging_setup
from orbsim.r4b_3d.mplotting import animate_r4b_orbitplot
from orbsim.r4b_3d.simulators import simulate

logging_setup()

logger = logging.getLogger()


if __name__ == "__main__":

    try:
        MODE = sys.argv[1]
    except IndexError:
        MODE = "leo"

    mode_dict = {
        # Keys: Possible input arguments (argv)
        # Values: Output folder name of associated log/figs of run
        # Simple simulation without burn
        "leo": "demo_leo",
        "sun": "demo_circular_sun_orbit",
    }

    MODE_NAME = mode_dict[MODE]
    OUTPUT_DIR = "runs/r4b_3d/" + MODE_NAME + "/"
    pathlib.Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    # Run simulate() with some initial conditions
    if MODE_NAME == "demo_leo":
        # Simple LEO without burn
        day = 0
        Q0, B0 = get_leo_position_and_velocity(day=day, altitude=160, end_year="2020")
        psi = (day, Q0, B0, None)
        h = 60 / UNIT_TIME  # step size
        ts, Qs, Bs, (t_final, i_final), ephemerides = simulate(
            psi=psi, max_year="2020", h=h, max_duration=0.003, max_iter=1e6
        )

    elif MODE_NAME == "demo_circular_sun_orbit":

        # Simple LEO without burn
        day = 0
        Q0, B0 = get_circular_sun_orbit_position_and_velocity()
        psi = (day, Q0, B0, None)
        h = 3600 * 12 / UNIT_TIME  # step size

        ts, Qs, Bs, (t_final, i_final), ephemerides = simulate(
            psi=psi, max_year="2039", h=h, max_duration=1, max_iter=1e6
        )

    # PLOT THINGS
    fig = plt.figure()
    animate_r4b_orbitplot(Qs, ts, t_final, fig)

