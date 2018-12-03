from orbsim.r3b_2d.simulators import run_sim

import matplotlib.pyplot as plt

import numpy as np

# from orbsim.plotting import orbitplot2d, orbitplot_non_inertial
# from numba import njit
from math import pi

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

eval_budget = 1000
best_run = {"score": 100.0, "success": False}
timeline = []
for i in range(eval_budget):
    psi = [random_disjoint_intervals(bound) for bound in bounds.values()]
    score, success, _ = run_sim(psi, duration=1, max_iter=1e7)
    score += psi[2]
    if not success:
        score = (score + 1) * 10

    if score < best_run["score"]:
        best_run["score"] = score
        best_run["success"] = success

    timeline.append(best_run["score"])

fig = plt.figure()
axrand = fig.add_subplot("121")
axevos = fig.add_subplot("122")
axrand.plot(timeline, color="black")
axevos.plot(range(len(timeline)), color="red")
plt.show()

