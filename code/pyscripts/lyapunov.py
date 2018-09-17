
# coding: utf-8

# In[5]:


import matplotlib.pyplot as plt
import numpy as np
from orbsim.r3b_2d.analyticals import *
from orbsim.r3b_2d.simulators import launch_sim
from orbsim.plotting import orbitplot2d, orbitplot_non_inertial, multi_plot
from orbsim import *
from orbsim.r3b_2d import *


# In[25]:


N = 4
examples = [
    # ["hohmann", [-2.086814820119193, -0.000122173047640, 3.111181716545691], 5],
    ["long_leto", [3.794182930145708, 0.023901745288554, 3.090702702702703], 200],
    # ["short_leto", [-0.138042744751570, -0.144259374836607, 3.127288444444444], 41],
    # ["3-day_hohmann", [-2.272183066647597, -0.075821466029764, 3.135519748743719], 3],
    # ["1-day_hohmann", [-2.277654673852600, 0.047996554429844, 3.810000000000000], 1],
]  # [title, psi, duration]
for title, psi, duration in examples:
    psis = []
    paths = []
    for i in range(N):
        permute_psi = np.array(psi) + np.array([i * 1e-6, i * 1e-6, i * 1e-6])
        path = launch_sim(permute_psi, max_iter=1e7, duration=duration)
        psis.append(permute_psi)
        paths.append(path)

    # In[26]:

    for i in range(len(paths)):
        orbitplot2d(
            paths[i],
            psis[i],
            filepath="./lyapunov_figs/trajectories",
            title=f"{title}_{i}",
        )
        orbitplot_non_inertial(
            paths[i],
            psis[i],
            filepath="./lyapunov_figs/trajectories",
            title=f"{title}_nonin_{i}",
        )

    # In[ ]:

    lyaps = []
    for a in range(N):
        for b in range(N):
            print(f"comparing {a} and {b}")
            if a >= b:
                continue
            multi_plot(
                [paths[a], paths[b]],
                [psis[a], psis[b]],
                orbitplot2d,
                filepath="./lyapunov_figs/trajectories",
                title=f"{title}_multi_{a}_and_{b}",
            )
            multi_plot(
                [paths[a], paths[b]],
                [psis[a], psis[b]],
                orbitplot_non_inertial,
                filepath="./lyapunov_figs/trajectories",
                title=f"{title}_nonin_multi_{a}_and_{b}",
            )
            plt.close('all')
            lyap = []
            _a = np.array(paths[a][1]).T
            _b = np.array(paths[b][1]).T
            xas = _a[0]
            yas = _a[1]
            xbs = _b[0]
            ybs = _b[1]
            #         hs=(_a[4],_b[4])
            ts = (_a[5], _b[5])
            print(
                f"length of the trajectory coordinate arrays: {a}: {len(xas)}, {b}: {len(xbs)}"
            )

            _, min_ts = min([(len(x), list(x)) for x in list(ts)])
            print(
                f"time steps standardized: comparing at {len(min_ts)} points on the trajectory. Last point will be at {max(min_ts)}"
            )
            for idx in range(len(min_ts)):
                #             idx=min_ts[i]
                lyap.append(
                    sqrt((xas[idx] - xbs[idx]) ** 2 + (yas[idx] - ybs[idx]) ** 2)
                )
            lyaps.append(lyap)
    print(len(lyaps))

    # In[ ]:

    loglyaps = []
    for i in range(len(lyaps)):
        lyap = lyaps[i][1:]
        loglyap = [np.log(x) for x in lyap]
        loglyaps.append(loglyap)

    # In[ ]:

    def find_segments(lyap):
        segments = []
        prev_l = -1e8
        rising = True
        segment = [0]
        for i, l in enumerate(lyap):
            if rising:
                if l < prev_l:
                    rising = False
                    segment.append(i)
            else:
                if l > prev_l:
                    rising = True
                    segments.append(segment)
                    segment = [i]
            prev_l = l
        if len(segment) == 1:
            segment.append(len(lyap))
        segments.append(segment)
        return segments

    # In[ ]:

    from scipy import stats

    def compute_slope(lyap, filepath=".", title="derp"):
        segments = find_segments(lyap)
        plt.plot(range(len(lyap)), lyap, color="grey", alpha=0.5)
        slopes = []
        for lb, ub in [[int(x), int(y)] for [x, y] in segments]:
            if ub - lb < 100:
                continue
            if ub > len(lyap):
                break
            slope, intercept, r_value, p_value, std_err = stats.linregress(
                range(lb, ub), lyap[lb:ub]
            )
            slopes.append(slope)
            # print(slope, intercept)
            line = slope * range(lb, ub) + intercept
            plt.plot([lb, ub], [line[0], line[-1]], color="darkred")
            plt.plot(range(lb, ub), lyap[lb:ub], color="teal")
        mean_slope = np.mean(slopes)
        plt.suptitle(f"mean slope = {mean_slope}")
        plt.savefig(f"{filepath}/{title}.pdf")
        plt.clf()
        return mean_slope

    # In[ ]:

    slopes = []
    for i, loglyap in enumerate(loglyaps):
        slopes.append(
            compute_slope(
                loglyap, filepath="lyapunov_figs/slopes", title=f"{title}_{i}"
            )
        )
    print(f"mean slope = {np.mean(slopes)}")

    for i, lyap in enumerate(lyaps):
        print(title)
        print(
            f"max_dist={max(lyap)}\nmin_dist={min(lyap[1:])}\nmean_dist={np.mean(lyap)}\n"
        )

