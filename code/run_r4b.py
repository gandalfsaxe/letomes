"""Run the R4B simulator"""

import logging

import matplotlib.pyplot as plt

from orbsim.r4b_3d import UNIT_TIME

from orbsim.r4b_3d.mplotting import animate_r4b_orbitplot, r4b_orbitplot

from orbsim.r4b_3d.logging import logging_setup
from orbsim.r4b_3d.simulators import simulate

logging_setup()

logger = logging.getLogger()


if __name__ == "__main__":

    ts, Qs, Bs, (t_final, i_final), ephemerides = simulate(
        h=10 / UNIT_TIME, max_duration=1 * 3600 * 3 / UNIT_TIME, max_iter=1e6
    )

    fig = plt.figure()
    ax = fig.add_subplot("111", projection="3d")
    animate_r4b_orbitplot(Qs, t_final, fig, ax)

    fig = plt.figure()
    ax = fig.add_subplot("111", projection="3d")
    r4b_orbitplot(Qs, ax)
    plt.show()
