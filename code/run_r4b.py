"""Run the R4B simulator"""

import logging

from orbsim.r4b_3d import UNIT_TIME

# from orbsim.r4b_3d.logging import logging_setup
from orbsim.r4b_3d.simulators import simulate

# logging_setup()

logger = logging.getLogger()


if __name__ == "__main__":

    qs, ps, (t, i), ephemerides = simulate(
        h=10 / UNIT_TIME, max_duration=1 * 3600 * 6 / UNIT_TIME, max_iter=1e6
    )

    pass
