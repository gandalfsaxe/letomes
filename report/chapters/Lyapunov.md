# Sensitivity analysis

In our experiments, we found that our paths were diverging pretty heavily given relatively small changes to initial conditions. This was a concern in the original project as well, but was not fully explored then. It is important to quantify the chaotic nature of a system like this, since we are dealing with numerical simulation, which will always have some error associated with it. One takes steps to minimize such errors, often sacrificing computing performance to do so. However, if a system has an error of magnitude say 1e-8, and the system is so chaotic that errors of 1e-9 at one point early in the trajectory effect meaningful changes further down the line, then the path is near invalid! Therefore, it is important to try to quantify the chaos of a system (in this case our simulator), to provide assurances that the resulting paths have any meaningful truth to them. We have done this by calculating Lyapunov exponents for the system, explained below.

## Lyapunov Exponent

The Lyapunov exponent describes the rate of change as time goes on between time series with infinitesimally different starting conditions, as they progress. The method is to compute a set of trajectories, and take the difference between them at set points in time (euclidean distance when dealing with higher dimensions). In a chaotic system, these two trajectories should diverge from each other at some exponential rate, and the Lyapunov exponent is that rate. If we want to trust our results, we want that number to be as low as possible. 

## Implementation

We ran several simulations of known good trajectories, with their starting conditions very slightly perturbed, in such a way that the trajectories initially diverged from each other by a value less that 1e-8, chosen as the square root of the precision of the 64-bit floating point numbers that describe the coordinates. The trajectories were then discretized to syncronize the variable length of the time steps, and then compared in pairs, tick by tick, yielding a list of euclidean distances at each step. We then took the natural logarithm of these lists, giving us the graph pictured in figure \ref{lyapunov}. The graph varied heavily depending on the gist of the trajectory in question, with trajectories that made multiple passes near earth giving the tooth-like distance graphs pictured in fig. \ref{lyapunov_a}. Trajectories that did not visit earth more than once gave much more 'normal' results, given what we see in the literature pertaining to Lyapunov exponent analysis. Clearly, passing into the LEO domain has a powerful stabilizing effect on the the chaotic system, acting like a focal lens for the trajectories passing through. It's not completely trivial to give a Lyapunov exponent from this, but since the individual tooth-segments have a more or less equivalent slope, we simply took the average slope of the first five teeth. A deeper look into this cyclical chaos would be interesting, but we did not delve deeper than this.

A good heuristic for whether or not our paths are precise enough would be a measure that would give some confidence interval for final position, given the gist of a trajectory, and the duration of flight along it. We have calculated somesuch measures, presented in fig. \ref{lyapunov_heuristic}