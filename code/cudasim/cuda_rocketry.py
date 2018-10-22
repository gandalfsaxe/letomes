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
from orbsim.r3b_2d.analyticals import (
    ensure_bounds,
    random_disjoint_intervals,
    collapse_intervals,
)
import time
from numba import jit, njit
import math
from math import pi
from scipy.stats import rankdata

# from ctypes import cdll
from ctypes import *

cudasim = cdll.LoadLibrary("./libcudasim.so")

pi8 = pi / 8
pi4 = pi / 4
pi2 = pi / 2
tau = 2 * pi


def evolve(psis, bounds, nIterations, nIndividuals, nJitter, maxDuration, maxSteps):
    init_sigma = 0.3  # spread
    init_alpha = 0.003  # learningrate
    sigma, alpha = init_sigma, init_alpha
    # sigma = np.ones(nIndividuals) * init_sigma
    # alpha = np.ones(nIndividuals) * init_alpha
    logfile = open(f"cudaES.log", "w")
    winners = []
    intermediate_winners = []
    bounds_list = bounds.values()
    for _ in range(nIterations):

        """
        make list of all paths to integrate
        """
        np.random.seed(0)
        jitter = np.random.rand(nIndividuals, nJitter, 3)
        jitter = np.array([sigma * jitt for idx, jitt in enumerate(jitter)])
        jitter = jitter.reshape(nJitter, nIndividuals, 3)
        jitter[0] *= 0  # Make sure all set individuals are evaluated without jitter
        points = jitter + psis
        points = points.reshape(nIndividuals * nJitter, 3)
        for i, pt in enumerate(points):
            points[i] = ensure_bounds(pt, bounds_list)
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
        points=points.reshape(nIndividuals*nJitter,3)
        for i, _ in enumerate(scores):
            scores[i] += points[i][2]
            if not successes[i]:
                scores[i] += 10
                scores[i] *= 10

        successes = successes.reshape(nJitter, nIndividuals)
        scores = scores.reshape(nIndividuals, nJitter)
        ranked_scores = np.array(
            [rankdata(sig_eps, method="ordinal") for sig_eps in scores]
        )
        ranked_scores = -ranked_scores

        steps = np.zeros([nIndividuals, 3])
        jitter = jitter.transpose(1, 0, 2)
        steps = np.array(
            [
                np.dot(ranked_scores[idx], jitter[idx]) * alpha
                for idx in range(len(steps))
            ]
        )

        successes = successes.reshape(nIndividuals, nJitter)
        points = points.reshape(nIndividuals, nJitter, 3)
        # scores = scores.reshape(nIndividuals, nJitter)
        for idx, psi in enumerate(psis):
            if successes[idx][0]:
                winners.append(str([idx, psi, scores[idx][0]]) + "\n")
            for jdx, succ in enumerate(successes[idx]):
                if succ:
                    intermediate_winners.append(
                        str(" -- " + [idx, points[idx][jdx], scores[idx][jdx]]) + "\n"
                    )

        psis += steps

    logfile.writelines(winners)
    logfile.close()


def initialize_psis(n, bounds):
    psis = [
        [random_disjoint_intervals(bound) for bound in bounds] for _ in range(n)
    ]
    return psis


if __name__ == "__main__":
    nIterations = 2
    nIndividuals = 1024
    nJitter = 32
    maxDuration = 7
    maxSteps = 10e6
    bounds = {
        "pos": np.array([[0, 0 * tau]]),
        "ang": np.array([[0, 1 * tau / 16], [tau / 2 - tau / 16, tau / 2]]),
        "burn": np.array([[3.2, 3.9]]),
    }
    psis = initialize_psis(nIndividuals, bounds.values())
    # pop.set_x(0, [-2.277654673852600, 0.047996554429844, 3.810000000000000])
    # pop.set_x(1, [-0.138042744751570, -0.144259374836607, 3.127288444444444])
    # pop.set_x(2, [-2.086814820119193, -0.000122173047640, 3.111181716545691])
    # print(pop)
    evolve(
        psis, bounds, nIterations, nIndividuals, nJitter, maxDuration, maxSteps
    )
