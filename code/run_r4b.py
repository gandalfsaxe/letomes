"""Run the R4B simulator"""

import logging

from orbsim.r4b_3d import UNIT_TIME
from orbsim.r4b_3d.initial_conditions import get_leo_position_and_velocity
from orbsim.r4b_3d.logging import logging_setup
from orbsim.r4b_3d.simulators import simulate

import matplotlib.pyplot as plt


from orbsim.r4b_3d.mplotting import animate_r4b_orbitplot, r4b_orbitplot


logging_setup()

logger = logging.getLogger()


if __name__ == "__main__":

    # Simple LEO without burn
    Q0, B0 = get_leo_position_and_velocity(day=0, altitude=160, end_year="2020")
    psi_leo = (0, Q0, B0, None)
    ts, Qs, Bs, (t_final, i_final), ephemerides = simulate(
        psi=psi_leo,
        h=10 / UNIT_TIME,
        max_duration=1 * 3600 * 3 / UNIT_TIME,
        max_iter=1e6,
    )

    fig = plt.figure()
    ax = fig.add_subplot("111", projection="3d")
    animate_r4b_orbitplot(Qs, t_final, fig, ax)

    fig = plt.figure()
    ax = fig.add_subplot("111", projection="3d")
    r4b_orbitplot(Qs, ax)
    plt.show()
