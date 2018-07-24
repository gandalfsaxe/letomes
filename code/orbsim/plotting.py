import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def orbitplot(completed_path):
    Dv, path = completed_path

    xs = [e[0] for e in path]
    ys = [e[1] for e in path]
    hs = [e[4] for e in path]
    fig = plt.figure()
    ax = fig.gca(projection="3d")
    fig.suptitle(f"DeltaV = {Dv}")
    ax.plot(xs, ys, hs)
    ax.plot(xs[0:2], ys[0:2], hs[0:2], color="green", linewidth=6)
    ax.plot(xs[-3:-1], ys[-3:-1], hs[-3:-1], color="red", linewidth=6)
    plt.show()
