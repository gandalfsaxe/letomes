from orbsim.r3b_2d.simulators import launch_sim
from multiprocessing import Pool

import matplotlib.pyplot as plt
import numpy as np
import pygmo as pg
from pygmo import algorithm
import os
import sys
from orbsim.r3b_2d.simulators import launch_sim
from orbsim.plotting import orbitplot2d, orbitplot_non_inertial
import time
from numba import jit, njit
import math
from math import pi

pi8 = pi / 8
pi4 = pi / 4
pi2 = pi / 2

@njit
def evolve(psis, iterations):
    sigma = 0.001
    alpha = 0.003  # learningrate

    # for each iteration, jitter around starting points, and move in the
    # best direction (weighted average jitter coordinates according to
    # fitness score)
    for i in range(iterations):

        # do the jittering and selection
        for psi in psis:
            noise = np.random.randn(10, 3)
            epsis = [
                [psi_0, psi_1, psi_2]
                for [psi_0, psi_1, psi_2] in np.expand_dims(psi, 0) + sigma * noise
            ]

            reward = np.array([-launch_sim(epsi, max_iter=1e7)[0] for epsi in epsis])
            reward -= reward.mean()
            reward /= reward.std()
            step_norm = np.dot(reward, noise)  # F, in the literature
            step = alpha * step_norm
            print(f"new individual = {str(psi+step)}")
            psi += step  # mutate the population/take the step
    return psis


class saddle_space:
    def __init__(self):
        pass

    def fitness(self, psi):
        res, _ = launch_sim(psi, duration=50, max_iter=1e7)
        return [-res]

    @jit
    def get_bounds(self):
        return ([-pi, -pi8, 2], [pi2, pi4, 4])


if __name__ == "__main__":
    p = Pool(4)
    # iterations=3
    prob = pg.problem(saddle_space())
    popu = pg.population(prob=prob, size=2)
    pop = popu.get_x()
    print(p.starmap(evolve, [(pop, 2), (pop, 4), (pop, 6), (pop, 8)]))
