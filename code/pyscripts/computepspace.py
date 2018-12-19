
from matplotlib.colors import Normalize
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

import pandas as pd

import numpy as np
from math import pi, log
from scipy.stats import rankdata
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("fp", type=str)
    parser.add_argument(
        "bounds", type=float, nargs=4, help="lowerbound x, upperbound x, lb y, ub y"
    )
    args = parser.parse_args()
    filepath = args.fp
    dims = args.bounds

    # === setup problem space, either real or Karpathy toy problem for validation ===
    # pspace = np.loadtxt("golf_course_zoom_s1024.txt")
    pspace = np.loadtxt(filepath)
    # uncomment this line if you want smooth toy-problem
    # pspace = G
    print(dims)
    lbp, ubp, lbb, ubb = dims

    # ******************** PLOTTING ****************************************
    # ======== establish figs =================
    fig = plt.figure()
    ax = fig.gca()

    # ============= plot problem space bg images ====
    cmap = plt.cm.viridis
    colors = Normalize(min(pspace.flatten()), max(pspace.flatten()))(pspace)
    colors = cmap(colors)
    plt.axis('equal')
    plt.imshow(
        colors,
        vmin=min(pspace.flatten()),
        vmax=max(pspace.flatten()),
        extent=[lbb, ubb,lbp, ubp],
        aspect="auto",
        interpolation="none",
        origin="lower",
    )
    ax.set_xlabel("burnDv")
    ax.set_ylabel("position")


    plt.colorbar()

    plt.show()

