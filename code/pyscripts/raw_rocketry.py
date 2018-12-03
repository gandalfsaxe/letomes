from orbsim.r3b_2d.simulators import run_sim
from multiprocessing import Pool
import multiprocessing as mp

import numpy as np
import pygmo as pg

# from orbsim.plotting import orbitplot2d, orbitplot_non_inertial
# from numba import njit
from math import pi
from scipy.stats import rankdata

from orbsim.r3b_2d.analyticals import (
    ensure_bounds,
    random_disjoint_intervals,
    collapse_intervals,
)

tau = pi * 2
bounds = {
    "pos": np.array([[3.8, 5.0]]),
    "ang": np.array([[0, 0.02]]),
    "burn": np.array([[3.1, 3.15]]),
}


# @njit
def evolve(psis):
    init_sigma = 0.003
    init_alpha = 0.0003  # learningrate
    init_psis = psis

    iterations = 50
    # for each iteration, jitter around starting points, and move in the
    # best direction (weighted average jitter coordinates according to
    # fitness score)
    for idx in range(len(psis)):
        sigma = init_sigma
        alpha = init_alpha
        final_scores = []
        for _ in range(iterations):
            psi = psis[idx]
            noise = np.random.randn(25, 3)
            epsis = psi + sigma * noise  # the point cloud around psi
            epsis = [ensure_bounds(epsi, bounds.values()) for epsi in epsis]

            """calculate the reward in the cloud"""
            score, success = fitness(psi)
            print(f"individual {idx}: {score}, {psi}")
            e_scores = np.zeros(len(epsis))
            e_successes = np.zeros(len(epsis))
            for jdx in range(len(epsis)):
                epsi = epsis[jdx]
                e_scores[jdx], e_successes[jdx] = fitness(
                    epsi
                )  # launch a simulation for each point
            ranked_scores = fitness_shape(epsis, e_scores, e_successes)

            step_norm = np.dot(
                -1 * ranked_scores, noise
            )  # problem is flipped from maximization to minimization here. (*-1)
            step = alpha * step_norm
            psis[idx] = psi + step  # mutate the population/take the step
            # sigma = min(1.2, init_sigma, init_sigma * (psi_reward * 8))
            # alpha = max(0.8, min(init_alpha, init_alpha * (psi_reward * 8)))
        final_scores.append(score)
    [
        print(
            f"psis[{idx}] went from {init_psis[idx]} to {psis[idx]} in {iterations} iterations, final score={final_scores[idx]}"
        )
        for idx in range(len(psis))
    ]
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


# @njit
def fitness_shape(psis, scores, successes):
    for idx in range(len(scores)):
        if successes[idx]:
            scores[idx] = scores[idx] + psis[idx][2]  # just add burnDv
        else:
            scores[idx] = scores[idx] + 20 + psis[idx][2]  # punish for not hitting

    ranked_scores = rankdata(scores)
    mean = ranked_scores.mean()
    ranked_scores -= mean
    ranked_scores /= ranked_scores.std()
    ranked_scores = [min(0, rscore) for rscore in ranked_scores]
    # neutralize negative influence by making very poor fitnesses equal to the mean fitness
    return np.array(ranked_scores).transpose()


# @njit
def fitness(psi):
    score, success, _ = run_sim(psi, duration=200, max_iter=1e7)
    return [score, success]


def initialize_psis(n, bounds):
    psis = [[random_disjoint_intervals(bound) for bound in bounds] for _ in range(n)]
    return psis


if __name__ == "__main__":
    mag = mp.cpu_count()
    nIndividuals = mag
    p = Pool(mag)
    nBuckets = mag
    # evolve(np.array(initialize_psis(nIndividuals, bounds.values())))
    result = p.map(
        evolve,
        [
            np.array(initialize_psis(int(nIndividuals / nBuckets), bounds.values()))
            for _ in range(mp.cpu_count())
        ],
    )
    print(result)
    # print(p.starmap(evolve, [(pop, 2), (pop, 4), (pop, 6), (pop, 8)]))
