"""Run the R4B simulator"""

import logging

import matplotlib.pyplot as plt

from orbsim.r4b_3d import UNIT_TIME
from orbsim.mplotting import animate_r4b_orbitplot, r4b_orbitplot

# from orbsim.r4b_3d.logging import logging_setup
from orbsim.r4b_3d.simulators import simulate

# logging_setup()

logger = logging.getLogger()


if __name__ == "__main__":

    ts, qs, ps, (t_final, i_final), ephemerides = simulate(
        h=10 / UNIT_TIME, max_duration=1 * 3600 * 3 / UNIT_TIME, max_iter=472
    )

    fig = plt.figure()
    ax = fig.add_subplot("111", projection="3d")
    animate_r4b_orbitplot(qs, fig, ax)

    fig = plt.figure()
    ax = fig.add_subplot("111", projection="3d")
    r4b_orbitplot(qs, ax)
    plt.show()
