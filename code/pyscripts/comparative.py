
from matplotlib.colors import Normalize
import matplotlib as mpl
import matplotlib.pyplot as plt

import numpy as np
from math import pi

pspace = np.loadtxt("golf_course_zoom.txt")
print(pspace)
dims = pspace.shape
print(dims)

tau = pi * 2
bounds = {
    "pos": np.array([[3.8, 5.0]]),
    "ang": np.array([[0, 0.02]]),
    "burn": np.array([[3.1, 3.15]]),
}


def evolve(startpsi, iterations, timeline):
    sigma = 5
    alpha = 0.5
    epsi_size = 25
    psi = startpsi
    for i in range(int(iterations / epsi_size)):
        noise = np.random.randn(epsi_size, 2).astype("int")
        x, y = psi
        x, y = [min(dims[0] - 1, max(0, x)), min(dims[1] - 1, max(0, y))]
        epsi = [x, y] + sigma * noise
        timeline.append({"score": pspace[int(x)][int(y)], "coords": [x, y]})

        R = np.array([-1 * pspace[int(x)][int(y)] for x, y in epsi])
        R -= R.mean()
        R /= R.std()
        step_norm = np.dot(R, noise)
        step = alpha * step_norm
        psi += step


eval_budget = 10000
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

    rg_timeline.append(best_run.copy())
    x_timeline.append(psi[0])
    y_timeline.append(psi[1])

es_timeline = []
startpsi = [np.random.randint(low=0, high=dim) for dim in dims]
evolve(startpsi, eval_budget, es_timeline)


fig = plt.figure()
axrand = fig.add_subplot("221")
axevos = fig.add_subplot("222")
ax_rg_pspace = fig.add_subplot("223")
ax_es_pspace = fig.add_subplot("224")
axrand.plot([best["score"] for best in rg_timeline], color="black")
axevos.plot([part["score"] for part in es_timeline], color="red")

cmap = plt.cm.jet
colors = Normalize(min(pspace.flatten()), max(pspace.flatten()))(pspace)
colors = cmap(colors)
im = ax_rg_pspace.imshow(
    colors,
    vmin=min(pspace.flatten()),
    vmax=max(pspace.flatten()),
    extent=[0, dims[0], 0, dims[1]],
    interpolation="none",
)
im2 = ax_es_pspace.imshow(
    colors,
    vmin=min(pspace.flatten()),
    vmax=max(pspace.flatten()),
    extent=[0, dims[0], 0, dims[1]],
    interpolation="none",
)

plt.colorbar(mappable=im, ax=ax_rg_pspace)
bestcoords = np.array([best["coords"] for best in rg_timeline]).T
ax_rg_pspace.scatter(bestcoords[0], bestcoords[1], color="lime", s=3)
ax_rg_pspace.scatter(x_timeline, y_timeline, color="black", s=0.2)

plt.colorbar(mappable=im2, ax=ax_es_pspace)
coords = np.array([part["coords"] for part in es_timeline]).T
ax_es_pspace.scatter(coords[0], coords[1], color="black", s=3)
plt.show()

