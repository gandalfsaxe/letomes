"""Run the R4B simulator"""

import logging
import pathlib
import sys

from math import pi, floor

import numpy as np
from numpy import arange

from orbsim import DAY
from orbsim.r4b_3d import UNIT_TIME

#from orbsim.r4b_3d.initial_conditions import (
#    get_leo_position_and_velocity,
#    get_circular_sun_orbit_position_and_velocity,
#)
from marscudasim.initial_conditions import (
    get_leo_positions_and_velocities,
    get_leo_positions_and_velocities_C,
)
from orbsim.r4b_3d.logging import logging_setup
from orbsim.r4b_3d.mplotting import all_plots_r4b_orbitplot
#from orbsim.r4b_3d.simulators import simulate as simulate_ref
from marscudasim.simulators import simulate, simulate_single

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
        "single": "leo_plot_single",
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
        #day = 0.0
        days = np.linspace(0.5, 365 + 364.5, 2 * 365)
        burndvs = np.linspace(2.52, 3.51, 100)

        # First refinement search
        day = 310.5 + 6 * 687 - 80
        dday = 20
        burn = 3.86
        dburn = 0.2
        tilt = (15.0 / 180.0) * pi
        dtilt = (15.0 / 180.0) * pi 

        # Second refinement search
        day = 4351.5
        dday = 1
        burn = 3.91
        dburn = 0.04
        tilt = 0.523598775598
        dtilt = 0.04

        # Specify search space
        days = np.linspace(day - dday, day + dday, 5)
        burndvs = np.linspace(burn - dburn, burn + dburn, 41)
        tilts = np.linspace(tilt - dtilt, tilt + dtilt, 81)

        max_year = "2039"
        h = 1 / UNIT_TIME # 0.1 seconds
        max_duration = 290 * DAY / UNIT_TIME
        max_iter = 100000000
        day0s, Q0s, B0s = get_leo_positions_and_velocities_C(days=days,
                                                             burndvs=burndvs,
                                                             tilts=tilts,
                                                             h=h,
                                                             altitude=160,
                                                             max_year=max_year)

        logging.info("-------------------------------------------- CPU -------------------------------------------------------------------")
        """
        ts, Qs, Bs, (t_final, i_final), ephemerides = simulate_ref(
            psi=(day, Q0, B0, None),
            max_year=max_year,
            h=h,
            max_duration=max_duration,
            max_iter=max_iter,
        )
        """
        logging.info("-------------------------------------------- GPU -------------------------------------------------------------------")

        arives, scores = simulate(
            psi=(day0s, Q0s, B0s, None),
            max_year=max_year,
            h=h,
            max_duration=max_duration,
            max_iter=max_iter,
        )
        print("Total paths=", len(scores))
        print("days=", days)
        print("burndvs=", burndvs)
        print("tilts=", tilts)
        bestscores = np.sort(scores)
        bestidx = np.argsort(scores)
        bestarives = arives[bestidx]
        for s in range(min(len(scores), 20)):
            n = bestidx[s]
            i = int(floor(n / (len(burndvs) * len(tilts))))
            m = n % (len(burndvs) * len(tilts))
            j = int(floor(m / len(tilts)))
            k = m % len(tilts)
            print("pathNo=", n,
                  "duration=", bestarives[s] - days[i],
                  "dmars=", bestscores[s], "km",
                  "| day=", days[i],
                  "burndv=", burndvs[j],
                  "tilt=", tilts[k],
                  "Q=", Q0s[n],
                  "B=", B0s[n])
            
            #best = list([bestidx[0:10], bestarivees[0:10], bestscores[0:10]])
            #print(best[0])
            #print(best[1])
            #print(best[2])

        """
        ts, Qs, Bs, (t_final, i_final), ephemerides = simulate(
            psi=(day, Q0, B0, None),
            max_year=max_year,
            h=h/2,
            max_duration=max_duration,
            max_iter=max_iter,
            number_of_paths=number_of_paths,
            fan_delta=fan_delta,
            coordinate_no=coordinate_no,
        )
        """
    elif MODE_NAME == "leo_plot_single":

        # Simple LEO without burn
        #day = 0.0
        days = np.array([271.5])
        burndvs = np.array([3.51])
        days = np.array([518.5])
        burndvs = np.array([4.1])

        # Mars hit trajectory
        days = np.array([4351.5])
        burndvs = np.array([0 * 3.918])
        tilts = np.array([0.557598775598])

        max_year = "2039"
        h = 1 / UNIT_TIME # 0.1 seconds
        max_duration = 300 * DAY / UNIT_TIME
        max_iter = 100000000
        day0s, Q0s, B0s = get_leo_positions_and_velocities(days=days,
                                                           burndvs=burndvs,
                                                           tilts=tilts,
                                                           h=h,
                                                           altitude=160,
                                                           max_year=max_year)
        ts, Qs, i_final = simulate_single(
            psi=(day0s, Q0s, B0s, None),
            max_year=max_year,
            h=h,
            max_duration=max_duration,
            max_iter=max_iter,
        )
        # PLOT THINGS
        i_final = i_final[0]
        i_plot = np.linspace(0, i_final - 1, min(1000, i_final)).astype(int)
        #print(i_final, UNIT_TIME * ts[i_final] / DAY, Qs[i_final])
        all_plots_r4b_orbitplot(Qs[i_plot,:], ts[i_plot], ts[i_final], max_year)
