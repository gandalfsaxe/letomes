
from matplotlib.colors import Normalize
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

import pandas as pd

import numpy as np
from math import pi, log
from scipy.stats import rankdata

# === setup problem space, either real or Karpathy toy problem for validation ===
pspace = np.loadtxt("golf_course_zoom_s1024.txt")
sz = 1024
X, Y = np.meshgrid(np.linspace(-1, 1, sz), np.linspace(-1, 1, sz))
mux, muy, sigma = 0.3, -0.3, 4
G1 = np.exp(-((X - mux) ** 2 + (Y - muy) ** 2) / 2.0 * sigma ** 2)
mux, muy, sigma = -0.3, 0.3, 2
G2 = np.exp(-((X - mux) ** 2 + (Y - muy) ** 2) / 2.0 * sigma ** 2)
mux, muy, sigma = 0.6, 0.6, 2
G3 = np.exp(-((X - mux) ** 2 + (Y - muy) ** 2) / 2.0 * sigma ** 2)
mux, muy, sigma = -0.4, -0.2, 3
G4 = np.exp(-((X - mux) ** 2 + (Y - muy) ** 2) / 2.0 * sigma ** 2)
G = G1 + G2 - G3 - G4

# uncomment this line if you want smooth toy-problem
# pspace = G
dims = pspace.shape
print(dims)

startpsi = [275,600]
np.random.seed(0)
# startpsi = [np.random.randint(low=0, high=dim) for dim in dims]
# sigma = 20
alpha = 0.2
epsi_size = 50
eval_budget = 2000

# +++++++++++++++++++++ Evolution Strategies ++++++++++++++++++++++++++++++
def evolve(startpsi, eval_budget, timeline):
    psi = startpsi
    sigma = 20
    best_score = 100.0
    for i in range(int(eval_budget / epsi_size)):
        noise = np.random.randn(epsi_size, 2)
        halfway = int(noise.shape[0]/2)
        for j in range(halfway):
            noise[halfway+j] = -1*noise[j]
        x, y = psi
        x, y = [min(dims[0] - 1, max(0, x)), min(dims[1] - 1, max(0, y))]
        epsi = [x, y] + sigma * noise
        epsi = [
            [min(dims[0] - 1, max(0, x)), min(dims[1] - 1, max(0, y))] for x, y in epsi
        ]

        score = pspace[int(x)][int(y)]
        if score < best_score:
            best_score = score

        R = np.array([-pspace[int(x)][int(y)] for x, y in epsi])
        R = np.array(rankdata(R), dtype=float)
        Rmean = R.mean()
        for idx, v in enumerate(R):
            if v<Rmean:
                R[idx]=0
        # print(R)
        R /= sum(R)
        step_norm = np.dot(R, noise)
        step = alpha * sigma**2 * step_norm
        sigma -= 0.4
        sigma = max(0,sigma)
        psi += step
        timeline.append(
            {
                "score": score,
                "best_score": best_score,
                "coords": [x, y],
                "step": step,
                "epsi": epsi,
            }
        )


es_timeline = []
evolve(startpsi, eval_budget, es_timeline)

# ===================== RANDOM GUESSING ==================================
best_run = {"score": 100.0, "coords": [0, 0]}
rg_timeline = []
x_timeline = []
y_timeline = []
for _ in range(eval_budget):
    psi = [np.random.randint(low=0, high=dim) for dim in dims]
    score = pspace[psi[0]][psi[1]]

    if score < best_run["score"]:
        best_run["score"] = score
        best_run["coords"] = psi

    rg_timeline.append(
        {"best_score": best_run["score"], "score": score, "coords": best_run["coords"]}
    )
    x_timeline.append(psi[0])
    y_timeline.append(psi[1])

# ******************** PLOTTING ****************************************
# ======== establish figs =================
fig = plt.figure()
axrand = fig.add_subplot("221")
axevos = fig.add_subplot("222")
ax_rg_pspace = fig.add_subplot("223")
ax_es_pspace = fig.add_subplot("224")

# ========= compute and plot convergence curves ==============
cummean = np.array(
    pd.Series([part["score"] for part in rg_timeline]).expanding().mean()
)
axrand.plot([part["best_score"] for part in rg_timeline], color="black")
axrand.plot(cummean, "b-")
axrand.plot([part["score"] for part in rg_timeline], color="red", alpha=0.4)

cummean = np.array(
    pd.Series([part["score"] for part in es_timeline]).expanding().mean()
)
axevos.plot([part["score"] for part in es_timeline], color="red", alpha=0.4)
axevos.plot(cummean, "b-")
axevos.plot([part["best_score"] for part in es_timeline], color="black")

# ============= plot problem space bg images ====
cmap = plt.cm.viridis
colors = Normalize(min(pspace.flatten()), max(pspace.flatten()))(pspace)
colors = cmap(colors)
im = ax_rg_pspace.imshow(
    colors,
    vmin=min(pspace.flatten()),
    vmax=max(pspace.flatten()),
    extent=[0, dims[0], 0, dims[1]],
    interpolation="none",
    origin='lower'
)
im2 = ax_es_pspace.imshow(
    colors,
    vmin=min(pspace.flatten()),
    vmax=max(pspace.flatten()),
    extent=[0, dims[0], 0, dims[1]],
    interpolation="none",
    origin='lower'
)

# ========= colorbars =========================
bestcoords = np.array([best["coords"] for best in rg_timeline]).T
ax_rg_pspace.scatter(x_timeline, y_timeline, color="black", s=0.2)
ax_rg_pspace.scatter(bestcoords[0], bestcoords[1], color="lime", s=3)

plt.colorbar(mappable=im2)
epsis = np.array([part["epsi"] for part in es_timeline])
coords = np.array([part["coords"] for part in es_timeline])
steps = np.array([part["step"] for part in es_timeline])

# ES timeline plot
# fig2 = plt.figure()
for idx, epsi in enumerate(epsis):
    ax_es_pspace.scatter(np.array(epsi).T[0], np.array(epsi).T[1], color="black", s=0.2)

ax_es_pspace.plot(coords.T[0], coords.T[1], "wo-")
ax_es_pspace.scatter(coords.T[0], coords.T[1], color="black", s=6)
arrow = [coords[-1], steps[-1]]
ax_es_pspace.arrow(
    arrow[0][0],
    arrow[0][1],
    arrow[1][0],
    arrow[1][1],
    head_width=3,
    head_length=5,
    fc="w",
    ec="w",
)


plt.show()

