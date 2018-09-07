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

#from ctypes import cdll
from ctypes import *
cudasim = cdll.LoadLibrary('./libcudasim.so')

pi8 = pi / 8
pi4 = pi / 4
pi2 = pi / 2

def evolve(phis, nIterations, nIndividuals, nJitter, maxDuration, maxSteps):
    sigma = 0.001
    alpha = 0.003  # learningrate

    """
    make list of all paths to integrate
    """

    # Try randn when it works, to see if better.           -----v
    np.random.seed(0)
    jitter = sigma * np.random.rand(nJitter, nIndividuals, 3)
    jitter *= saddle_space().get_ranges() # I put this here! Not in paper!
    jitter[0] *= 0 # Make sure all set island phis are evaluated without jitter
    points = jitter + phis
    success = np.zeros(nIndividuals * nJitter, dtype=bool)
    score = np.zeros(nIndividuals * nJitter)

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
    cudasim.integrate.argtypes = [c_int, c_int, c_double, c_int, POINTER(c_double), POINTER(c_bool), POINTER(c_double)]
    inArray = points.ctypes.data_as(POINTER(c_double))
    successArray = success.ctypes.data_as(POINTER(c_bool))
    scoreArray = score.ctypes.data_as(POINTER(c_double))
    cudasim.integrate(nIndividuals, nJitter, maxDuration, int(maxSteps), inArray, successArray, scoreArray)

    print("success=", success)
    print("score=", score)

class saddle_space:
    def __init__(self):
        pass

    def fitness(self, psi):
        #res, _ = launch_sim(psi, duration=50, max_iter=1e7)
        #return [-res]
        return [0]

    @jit
    def get_bounds(self):
        return ([-pi, -pi8, 2], [pi2, pi4, 4])

    @jit
    def get_ranges(self):
        bounds = self.get_bounds()
        return np.subtract(bounds[1], bounds[0])

if __name__ == "__main__":
    nIterations=1
    nIndividuals=1024
    nJitter=32
    maxDuration=5
    maxSteps=10e6
    prob = pg.problem(saddle_space())
    pop = pg.population(prob=prob, size=nIndividuals, seed=0)
    pop.set_x(0,[-2.277654673852600, 0.047996554429844, 3.810000000000000])
    pop.set_x(1,[-0.138042744751570, -0.144259374836607, 3.127288444444444])
    pop.set_x(2,[-2.086814820119193, -0.000122173047640, 3.111181716545691])
    # print(pop)
    evolve(pop.get_x(), nIterations, nIndividuals, nJitter, maxDuration, maxSteps)