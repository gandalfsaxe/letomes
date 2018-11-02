"""Run the R4B simulator"""

import logging

from orbsim.r4b_3d import UNIT_TIME

# from orbsim.r4b_3d.logging import logging_setup
from orbsim.r4b_3d.simulators import simulate

from orbsim.r4b_3d.plotting import r4b_plot

# logging_setup()

logger = logging.getLogger()


if __name__ == "__main__":

    ts, qs, ps, (t_final, i_final), ephemerides = simulate(
        h=10 / UNIT_TIME, max_duration=1 * 3600 * 3 / UNIT_TIME, max_iter=1e6
    )

    r4b_plot(t_final, ephemerides, qs)
