
import matplotlib as mpl
import matplotlib.pyplot as plt

import pandas as pd

import numpy as np
from math import log

np.random.seed(1)
scores = np.array(np.loadtxt("cuda_moon_scores.txt"))
print(scores.shape)
# x = range(scores.shape[0])
Niter = 1000
x = range(Niter)
for idx in np.random.randint(0, scores.shape[1], 3):
    timeline = scores.T[idx]
    logt = [log(t) for t in timeline[:Niter]]
    plt.plot(x, logt)
ax = plt.gca()
ax.set_xlabel("iterations")
ax.set_ylabel("log(fitness)")
plt.show()

