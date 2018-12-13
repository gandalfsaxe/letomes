
from orbsim.r3b_2d.simulators import run_sim

from multiprocessing import Pool
import multiprocessing as mp
from numba import njit
import datetime

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import numpy as np
from math import pi, log

tau = 2 * pi

filename = "golf_course_extrazoom_s300"


@njit
def run_with_scaled_score(psi):
    score, success, _ = run_sim(psi, duration=200, max_iter=1e7)
    if not success:
        score += 1
        score *= 10
    score += psi[2]
    score = log(score)
    return score, success


@njit
def golfcourse_row(pos, burns):
    result = [run_with_scaled_score([pos, 0.023901745288554, burn]) for burn in burns]
    return result


if __name__ == "__main__":
    sz = 300
    lbp, ubp = [4.8, 5.0]
    lbb, ubb = [3.1, 3.11]
    p = Pool(mp.cpu_count())
    poss = np.linspace(lbp, ubp, sz)
    burns = np.linspace(lbb, ubb, sz)
    result = np.array(
        p.starmap(golfcourse_row, [(poss[idx], burns) for idx in range(sz)])
    )

    cmap = plt.cm.viridis
    scores, successes = result.transpose(2, 0, 1)

    with open(f"{filename}.txt", "w") as matfile:
        smatrix = scores.reshape(sz, sz)
        np.savetxt(matfile, smatrix, fmt="%.4f")

    greys = np.empty(scores.shape + (3,), dtype=np.uint8)
    greys.fill(70)
    colors = Normalize(min(scores.flatten()), max(scores.flatten()))(scores)
    colors = cmap(colors)
    alphas = [[1 if succ else .4 for succ in alpharow] for alpharow in successes]

    colors[..., -1] = alphas

    fig, ax = plt.subplots()
    plt.imshow(greys)
    plt.imshow(
        colors,
        vmin=min(scores.flatten()),
        vmax=max(scores.flatten()),
        extent=[lbb, ubb, lbp, ubp],
        interpolation="none",
    )
    plt.colorbar()
    ax.set_xlabel("burnDv")
    ax.set_ylabel("position")
    ax.set_aspect((ubb - lbb) / (ubp - lbp))

    plt.savefig(f"{filename}.png")
