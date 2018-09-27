from orbsim.r3b_2d.simulators import run_sim
from multiprocessing import Pool

import matplotlib.pyplot as plt
import numpy as np
import pygmo as pg
from pygmo import algorithm
import os
import sys
from orbsim.r3b_2d.simulators import run_sim
from orbsim.plotting import orbitplot2d, orbitplot_non_inertial
import time
from numba import jit, njit
import math
from math import pi

# from ctypes import cdll
from ctypes import *

cudasim = cdll.LoadLibrary("./libcudasim.so")

pi8 = pi / 8
pi4 = pi / 4
pi2 = pi / 2


def evolve(psis, nIterations, nIndividuals, nJitter, maxDuration, maxSteps):
    init_sigma = 0.1  # spread
    init_alpha = 0.03  # learningrate

    sigma = np.ones(nIndividuals) * init_sigma
    alpha = np.ones(nIndividuals) * init_alpha
    logfile = open(f"cudaES.log", "w")
    winners = []
    intermediate_winners = []
    for _ in range(nIterations):

        """
        make list of all paths to integrate
        """
        # Try randn when it works, to see if better.           -----v
        np.random.seed(0)
        jitter = np.random.rand(nIndividuals, nJitter, 3)
        jitter = np.array([sigma[idx] * jitt for idx, jitt in enumerate(jitter)])
        jitter = jitter.reshape(nJitter, nIndividuals, 3)
        jitter[0] *= 0  # Make sure all set island phis are evaluated without jitter
        points = jitter + psis
        # jitter = [sigma[idx] * jitt for idx, jitt in enumerate(jitter)]
        # jitter *= saddle_space().get_ranges()  # I put this here! Not in paper!
        points = points.reshape(nIndividuals * nJitter, 3)
        for i, pt in enumerate(points):
            points[i] = ensure_bounds(pt)
        points = points.reshape(nJitter, nIndividuals, 3)
        successes = np.zeros(nIndividuals * nJitter, dtype=bool)
        scores = np.zeros(nIndividuals * nJitter)

        """
        cudasim.integrate
        
        Input:
        nIndividuals    Number of individuals (size of population)
        nJitter         Number of random jitter points
        maxSteps        Maximum number of steps of integration algorithm
        maxDuration     Maximum t (in days) of integration algorithm
        inArray         1D input array of doubles; size is 3 x nIndividuals 

        Output:
        successArray    1D ouput array of bools; size is 1 x nIndividuals
        scoreArray      1D ouput array of doubles; size is 1 x nIndividuals
        
        """
        cudasim.integrate.restype = None
        cudasim.integrate.argtypes = [
            c_int,
            c_int,
            c_double,
            c_int,
            POINTER(c_double),
            POINTER(c_bool),
            POINTER(c_double),
        ]
        inArray = points.ctypes.data_as(POINTER(c_double))
        successArray = successes.ctypes.data_as(POINTER(c_bool))
        scoreArray = scores.ctypes.data_as(POINTER(c_double))
        cudasim.integrate(
            nIndividuals,
            nJitter,
            maxDuration,
            int(maxSteps),
            inArray,
            successArray,
            scoreArray,
        )

        print("successes=", successes.sum())

        points = points.reshape(nIndividuals * nJitter, 3)
        for idx, _ in enumerate(scores):
            scores[idx] = -(
                scores[idx] + points[idx][2]
            )  # add burnDv to score and negate score since we are trying to minimize it

            if not successes[idx]:
                # punish paths that do not hit planet
                # sigma[idx] = init_sigma * 10
                # alpha[idx] = init_alpha * 10
                scores[idx] = -((scores[idx] - 10) ** 2)

        scores -= scores.mean()
        scores /= scores.std()
        print("scores=", scores, scores.shape)

        # # find successes and log them
        # winners = np.array(
        #     [
        #         (points[idx], scores.reshape(nIndividuals * nJitter)[idx])
        #         for idx, success in enumerate(successes)
        #         if success
        #     ]
        # )
        # for psi, score in winners:
        #     logfile.write(f"{psi}, {score}\n")

        # generate steps for next generation
        steps = np.zeros([nIndividuals, 3])
        scores = scores.reshape(nIndividuals, nJitter)
        jitter = jitter.reshape(nIndividuals, nJitter, 3)
        for idx in range(nIndividuals):
            steps[idx] = np.dot(scores[idx], jitter[idx]) * alpha[idx]

        # psi_scores = scores.T[0]
        # for idx, score in enumerate(psi_scores):
        #     sigma[idx] = init_sigma
        #     alpha[idx] = init_alpha

        successes = successes.reshape(nIndividuals, nJitter)
        points = points.reshape(nIndividuals, nJitter, 3)
        # scores = scores.reshape(nIndividuals, nJitter)
        for idx, psi in enumerate(psis):
            if successes[idx][0]:
                winners.append(str([idx, psi, scores[idx][0]]) + "\n")
            for jdx, succ in enumerate(successes[idx]):
                if succ:
                    intermediate_winners.append(
                        str([idx, points[idx][jdx], scores[idx][jdx]]) + "\n"
                    )

        psis += steps

    logfile.writelines(winners)
    logfile.close()


class saddle_space:
    def __init__(self):
        pass

    def fitness(self, psi):
        # res, _ = launch_sim(psi, duration=50, max_iter=1e7)
        # return [-res]
        return [0]

    @jit
    def get_bounds(self):
        return ([0, 0, 3], [2 * pi, 2 * pi, 4])

    @jit
    def get_ranges(self):
        bounds = self.get_bounds()
        return np.subtract(bounds[1], bounds[0])


@njit
def ensure_bounds(pt):
    pos, ang, burn = pt
    lb, ub = ([0, 0, 3], [2 * pi, 2 * pi, 4])
    return [
        np.mod(pos, ub[0] - lb[0]),
        np.mod(ang, ub[1] - lb[1]),
        max(lb[2], min(ub[2], burn)),
    ]


if __name__ == "__main__":
    nIterations = 100
    nIndividuals = 1024
    nJitter = 32
    maxDuration = 7
    maxSteps = 10e6
    prob = pg.problem(saddle_space())
    pop = pg.population(prob=prob, size=nIndividuals)
    # pop.set_x(0, [-2.277654673852600, 0.047996554429844, 3.810000000000000])
    # pop.set_x(1, [-0.138042744751570, -0.144259374836607, 3.127288444444444])
    # pop.set_x(2, [-2.086814820119193, -0.000122173047640, 3.111181716545691])
    # print(pop)
    evolve(pop.get_x(), nIterations, nIndividuals, nJitter, maxDuration, maxSteps)
