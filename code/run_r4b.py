"""Run the R4B simulator"""

import logging

from orbsim.r4b_3d.logging import logging_setup
from orbsim.r4b_3d.simulators import simulate

logging_setup()

logger = logging.getLogger()


if __name__ == "__main__":

    simulate()
