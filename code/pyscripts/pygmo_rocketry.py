
# coding: utf-8

# In[5]:


import numpy as np
import pygmo as pg
from pygmo import algorithm
import os
import sys
import json
from orbsim.r3b_2d import *
from orbsim.r3b_2d.analyticals import *
from orbsim.r3b_2d.simulators import launch_sim
from time import time
from random import shuffle
import math
from numba import njit, jit
from orbsim.plotting import orbitplot2d


# In[6]:


class saddle_space:
    def __init__(self):
        pass

    def fitness(self, psi):
        res, _ = launch_sim(psi, max_iter=1e6)
        return [res]

    def get_bounds(self):
        return ([-pi, -pi, -4], [pi, pi, 4])

    def get_name(self):
        return f"saddlespace"

    def plot(self, w, idx):
        pass


# In[7]:


class salimans_nes:
    def __init__(self, problem, iter=12):
        super(salimans_nes, self).__init__()
        self.prevx, self.prevy = [], []
        self.problem = problem

        self.iter = iter  # number of steps towards estimated gradient

    def evolve(self, pop):
        if len(pop) == 0:
            return pop
        sigma = 0.5
        alpha = 0.3  # learningrate

        # for each iteration, jitter around starting points, and move in the
        # best direction (weighted average jitter coordinates according to
        # fitness score)
        for i in range(self.iter):

            # get the population
            wl = pop.get_x()

            # do the jittering and selection
            j = 0
            for w in wl:
                print(f"mutating {str(w)}")
                noise = np.random.randn(5, 3)
                wp = [[x, y, z] for [x, y, z] in np.expand_dims(w, 0) + sigma * noise]
                print(np.expand_dims(w, 0) + sigma * noise)

                R = [launch_sim(wi)[0] for wi in wp]
                R -= R.mean()
                R /= R.std()
                g = np.dot(R, noise)
                u = alpha * g
                print(f"new individual = {str(u)}")
                w += u  # mutate the population

                pop.set_x(j, w)  # make the move previously selected
                j += 1
        return pop

    def get_name(self):
        return f"Oisin's big-dick omegafantastic algorithm"


# In[8]:


def pygmo_es():
    udp = saddle_space()  # user defined problem
    uda = salimans_nes(udp, iter=25)  # user defined algorithm  # Beautiful white snow

    archi = pg.archipelago(algo=uda, prob=udp, n=1, pop_size=1)
    archi.evolve()
    sols = archi.get_champions_f()
    idx = sols.index(min(sols))
    print("Done!! Solutions found are: ")
    print(archi.get_champions_f())
    # udp.plot(archi.get_champions_x(),idx)

    # pop = pg.population(prob,10,3)
    # algo.evolve(pop)


# In[9]:


if __name__ == "__main__":
    start = time()
    pygmo_es()
    print(time() - start)

