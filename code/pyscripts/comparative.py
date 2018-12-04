
from matplotlib.colors import Normalize
import matplotlib as mpl
import matplotlib.pyplot as plt

import numpy as np
from math import pi

pspace = np.loadtxt("golf_course_zoom.txt")
print(pspace)
dims = pspace.shape

tau = pi * 2
bounds = {
    "pos": np.array([[3.8, 5.0]]),
    "ang": np.array([[0, 0.02]]),
    "burn": np.array([[3.1, 3.15]]),
}

eval_budget = 1000
best_run = {"score": 100.0, "coords": [0, 0]}
timeline = []
x_timeline = []
y_timeline = []
for _ in range(eval_budget):
    psi = [np.random.randint(low=0, high=dim) for dim in dims]
    score = pspace[psi[0]][psi[1]]

    if score < best_run["score"]:
        best_run["score"] = score
        best_run["coords"] = psi

    timeline.append(best_run.copy())
    x_timeline.append(psi[0])
    y_timeline.append(psi[1])

fig = plt.figure()
axrand = fig.add_subplot("221")
axevos = fig.add_subplot("222")
axpspace = fig.add_subplot("223")
axrand.plot([best["score"] for best in timeline], color="black")
axevos.plot(range(len(timeline)), color="red")

cmap = plt.cm.jet
colors = Normalize(min(pspace.flatten()), max(pspace.flatten()))(pspace)
colors = cmap(colors)
im = axpspace.imshow(
    colors,
    vmin=min(pspace.flatten()),
    vmax=max(pspace.flatten()),
    extent=[0, dims[0], 0, dims[1]],
    interpolation="none",
)
plt.colorbar(mappable=im, ax=axpspace)
bestcoords = np.array([best["coords"] for best in timeline]).T
axpspace.scatter(bestcoords[0], bestcoords[1], color="lime", s=3)
axpspace.scatter(x_timeline, y_timeline, color="black", s=0.2)
plt.show()


def evolve(startpsi, iterations):
    sigma = 3
    alpha = 0.03
    psi = startpsi
    for i in range(iterations):
        noise = np.random.randn(25, 2)
        x, y = psi
        epsi = [min(dims[0], max(0, x)), min(dims[1], max(0, y))] + sigma * noise

        R = np.array([pspace[x][y] for x, y in epsi])
        R -= R.mean()
        R /= R.std()
        step_norm = np.dot(R, noise)
        step = alpha * step_norm
        psi += step

