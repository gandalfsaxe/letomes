"""Run the R4B simulator"""

import logging
import pathlib
import sys

from orbsim.r4b_3d import UNIT_TIME

from orbsim.r4b_3d.initial_conditions import (
    get_circular_sun_orbit_position_and_velocity,
    get_leo_position_and_velocity,
)
from orbsim.r4b_3d.logging import logging_setup
from orbsim.r4b_3d.mplotting import all_plots_r4b_orbitplot
from orbsim.r4b_3d.simulation import simulate

logging_setup()

logger = logging.getLogger()


if __name__ == "__main__":

    try:
        MODE = sys.argv[1]
    except IndexError:
        MODE = "leo"  # <-- INPUT DEMO / SEARCH PARAMETER HERE

    mode_dict = {
        # Keys: Possible input arguments (argv)
        # Values: Output folder name of associated log/figs of run
        # Simple simulation without burn
        "leo": "demo_leo",
        "sun": "demo_circular_sun_orbit",
        "mars": "demo_mars_transfer",
    }

    MODE_NAME = mode_dict[MODE]
    OUTPUT_DIR = "runs/r4b_3d/" + MODE_NAME + "/"
    pathlib.Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    # Run simulate() with some initial conditions
    if MODE_NAME == "demo_leo":
        # Simple LEO without burn
        day = 0
        max_year = "2020"
        h = 1 * 30 / UNIT_TIME
        max_duration = 3600 * 12 / UNIT_TIME
        max_iter = 1e6

        Q0, B0 = get_leo_position_and_velocity(day=day, altitude=160, max_year=max_year)
        ts, Qs, Bs, (
            t_final,
            i_final,
        ), ephemerides, eph_body_coords, body_distances = simulate(
            psi=(day, Q0, B0, None),
            max_year=max_year,
            h=h,
            max_duration=max_duration,
            max_iter=max_iter,
        )

    elif MODE_NAME == "demo_circular_sun_orbit":
        # Simple circular orbit around sun, pos (1,0,0) AU, unit vel (0,1,0)
        day = 0
        max_year = "2039"
        h = 3600 * 24 / UNIT_TIME
        max_duration = 1
        max_iter = 1e6

        Q0, B0 = get_circular_sun_orbit_position_and_velocity()
        ts, Qs, Bs, (
            t_final,
            i_final,
        ), ephemerides, eph_body_coords, body_distances = simulate(
            psi=(day, Q0, B0, None),
            max_year=max_year,
            h=h,
            max_duration=max_duration,
            max_iter=max_iter,
        )

    elif MODE_NAME == "demo_mars_transfer":
        # # Hohmann transfer orbit to Mars
        day = 50
        max_year = "2039"
        h = 60 / UNIT_TIME
        # max_duration = 3600 * 24 * 300 / UNIT_TIME
        max_duration = 3600 * 24 * 200 / UNIT_TIME
        max_iter = 1e6
        burn0 = 3.62  # burn delta-v in km/s

        Q0, B0 = get_leo_position_and_velocity(day=day, altitude=160, max_year=max_year)
        ts, Qs, Bs, (
            t_final,
            i_final,
        ), ephemerides, eph_body_coords, body_distances = simulate(
            psi=(day, Q0, B0, burn0),
            max_year=max_year,
            h=h,
            max_duration=max_duration,
            max_iter=max_iter,
        )

    # PLOT THINGS
    all_plots_r4b_orbitplot(Qs, ts, t_final, max_year)
