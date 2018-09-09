from orbsim.r3b_2d.simulators import launch_sim
from multiprocessing import Pool
import multiprocessing as mp

import numpy as np
import pygmo as pg
from orbsim.plotting import orbitplot2d, orbitplot_non_inertial
from numba import njit  # , njit
from math import pi

pi8 = pi / 8
pi4 = pi / 4
pi2 = pi / 2
pix2 = pi * 2


@njit
def evolve(psis):
    init_sigma = 0.01
    init_alpha = 0.03  # learningrate

    iterations = 3
    # for each iteration, jitter around starting points, and move in the
    # best direction (weighted average jitter coordinates according to
    # fitness score)
    for idx in range(len(psis)):
        sigma = init_sigma
        alpha = init_alpha
        for _ in range(iterations):
            psi = psis[idx]
            noise = np.random.randn(10, 3)
            epsis = psi + sigma * noise  # the point cloud around psi

            """calculate the reward in the cloud"""
            psi_reward = -launch_sim(psi, duration=10, max_iter=1e7)[1]
            reward = np.zeros(len(epsis))
            for jdx in range(len(epsis)):
                epsi = epsis[jdx]
                reward[jdx] = -launch_sim(epsi, duration=10, max_iter=1e5)[
                    1
                ]  # launch a simulation for each point
            reward -= reward.mean()
            reward /= reward.std()

            step_norm = np.dot(reward, noise)
            step = alpha * step_norm
            print("new individual = ")
            print(psi + step)
            psis[idx] = psi + step  # mutate the population/take the step
            sigma = min(1.2, init_sigma, init_sigma * (psi_reward * 8))
            alpha = max(0.8, min(init_alpha, init_alpha * (psi_reward * 8)))
    return psis

    # for i in range(iterations):

    #     # do the jittering and selection
    #     for psi in psis:
    #         noise = np.random.randn(10, 3)
    #         epsis = [
    #             [psi_0, psi_1, psi_2]
    #             for [psi_0, psi_1, psi_2] in np.expand_dims(psi, 0)
    #             + sigma * noise
    #         ]

    #         reward = np.array(
    #             [-launch_sim(epsi, duration=10, max_iter=1e7)[0] for epsi in epsis]
    #         )
    #         reward -= reward.mean()
    #         reward /= reward.std()
    #         step_norm = np.dot(reward, noise)  # F, in the literature
    #         step = alpha * step_norm
    #         print("new individual = {str(psi+step)}")
    #         psi += step  # mutate the population/take the step
    # return 0


@njit
def scale_result(success, res):
    if success:
        return [-res]
    else:
        return [-((res * 10) ** 2)]


@njit
def fitness(psi):
    success, res, _ = launch_sim(psi, duration=50, max_iter=1e7)
    return scale_result(success, res)


@njit
def get_bounds():
    return ([0, -pi, 3], [pix2, 0, 4])


if __name__ == "__main__":
    p = Pool(mp.cpu_count())
    popu = [(0.0, 2.0, 3.1), (1.0, 1.0, 3.6), (0.0, -2.0, 3.1), (0.2, 2.4, 3.2)]
    pop = np.array(popu)
    result = p.map(evolve, [pop for _ in range(mp.cpu_count())])
    print(result)
    # print(p.starmap(evolve, [(pop, 2), (pop, 4), (pop, 6), (pop, 8)]))
