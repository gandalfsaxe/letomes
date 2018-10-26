
from orbsim.r3b_2d.simulators import run_sim

from multiprocessing import Pool
import multiprocessing as mp

from numba import jit, njit
import matplotlib.pyplot as plt
import numpy as np
from math import pi

tau = 2 * pi


@njit
def golfcourse_row(pos, burns):
    return [run_sim([pos, 0, burn], duration=7, max_iter=1e7)[0] for burn in burns]


if __name__ == "__main__":
    sz = 100
    p = Pool(mp.cpu_count())
    poss = np.linspace(-tau / 2, tau / 4, sz)
    burns = np.linspace(3.0, 4.2, sz)
    # print([(poss[idx], burns) for idx in range(sz)])
    result = np.array(
        p.starmap(golfcourse_row, [(poss[idx], burns) for idx in range(sz)])
    )
    fig, ax = plt.subplots()
    im = ax.imshow(
        result, vmin=min(result.flatten()), vmax=max(result.flatten()), cmap="jet"
    )
    plt.show()
