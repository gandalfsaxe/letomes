"""Run the R4B simulator"""

import logging
import pathlib
import sys

from orbsim.r4b_3d import UNIT_TIME
from orbsim.r4b_3d.initial_conditions import (
    get_leo_position_and_velocity,
    get_circular_sun_orbit_position_and_velocity,
)
from orbsim.r4b_3d.logging import logging_setup
#from orbsim.r4b_3d.mplotting import all_plots_r4b_orbitplot
from orbsim.r4b_3d.simulators import simulate as simulate_ref
from marscudasim.simulators import simulate

logging_setup()

logger = logging.getLogger()


if __name__ == "__main__":

    try:
        MODE = sys.argv[1]
    except IndexError:
        MODE = "multi"  # <-- INPUT DEMO / SEARCH PARAMETER HERE

    mode_dict = {
        # Keys: Possible input arguments (argv)
        # Values: Output folder name of associated log/figs of run
        # Simple simulation without burn
        "leo": "demo_leo",
        "sun": "demo_circular_sun_orbit",
        "multi": "leo_multiple_trajectories",
    }

    MODE_NAME = mode_dict[MODE]
    OUTPUT_DIR = "results/r4b_3d/" + MODE_NAME + "/"
    pathlib.Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    # Run simulate() with some initial conditions
    if MODE_NAME == "demo_leo":

        # Simple LEO without burn
        day = 0
        max_year = "2020"
        h = 60 / UNIT_TIME
        max_duration = 3600 * 24 / UNIT_TIME
        max_iter = 1e6

        Q0, B0 = get_leo_position_and_velocity(day=day, altitude=160, max_year=max_year)
        ts, Qs, Bs, (t_final, i_final), ephemerides = simulate(
            psi=(day, Q0, B0, None),
            max_year=max_year,
            h=h,
            max_duration=max_duration,
            max_iter=max_iter,
            number_of_paths=1,
            fan_delta=0,
            coordinate_no=0
        )

    elif MODE_NAME == "demo_circular_sun_orbit":

        # Simple circular orbit around sun, pos (1,0,0) AU, unit vel (0,1,0)
        day = 0
        max_year = "2039"
        h = 3600 * 24 / UNIT_TIME
        max_duration = 1
        max_iter = 1e6

        Q0, B0 = get_circular_sun_orbit_position_and_velocity()
        ts, Qs, Bs, (t_final, i_final), ephemerides = simulate(
            psi=(day, Q0, B0, None),
            max_year=max_year,
            h=h,
            max_duration=max_duration,
            max_iter=max_iter,
            number_of_paths=1,
            fan_delta=0,
            coordinate_no=0
        )

    elif MODE_NAME == "leo_multiple_trajectories":

        # Simple LEO without burn
        day = 0
        max_year = "2020"
        h = 60 / UNIT_TIME
        max_duration = 3600 * 24 / UNIT_TIME
        max_iter = 2001
        number_of_paths=100000
        fan_delta=0
        coordinate_no=1

        Q0, B0 = get_leo_position_and_velocity(day=day, altitude=160, max_year=max_year)

        logging.info("-------------------------------------------- CPU -------------------------------------------------------------------")

        ts, Qs, Bs, (t_final, i_final), ephemerides = simulate_ref(
            psi=(day, Q0, B0, None),
            max_year=max_year,
            h=h,
            max_duration=max_duration,
            max_iter=max_iter,
        )

        logging.info("-------------------------------------------- GPU -------------------------------------------------------------------")

        ts, Qs, Bs, (t_final, i_final), ephemerides = simulate(
            psi=(day, Q0, B0, None),
            max_year=max_year,
            h=h,
            max_duration=max_duration,
            max_iter=max_iter,
            number_of_paths=number_of_paths,
            fan_delta=fan_delta,
            coordinate_no=coordinate_no,

        )

    # PLOT THINGS
    #print(Qs, ts)
    #all_plots_r4b_orbitplot(Qs, ts, t_final, max_year)
