# Evolution Strategies

We are basing our machine learning efforts on the Evolution Strategy (ES) algorithm outlined by Salimans etal. **[ref]** using ES--it being a gradient estimator--makes sense in optimization scenarios where calculating an exact gradient is expensive. The idea is to sample around a starting point, and use a weighted average fitness score to pick a direction to move each cycle. It is generally applicable to unsupervised problems, such as ours; a reinforcement learning problem. There are several flavors of the concept under the ES umbrella term: Covariance Matrix Adaptation (CMA-ES), Natural Evolution Strategy (NES), and Exponential NES, to name a few. The one used in Salimans **[ref]** and by extension in our project is NES. Its exact implementation details will follow:

## NES Algorithm

In formal terms: Let $F$ be the objective function with parameters $\theta$. NES is the population from a distribution over parameters $p_\psi (\theta)$, with hyperparameters $\psi$. The procedure is then to optimize the expected objective value $E_{\theta \sim p_\psi} F(\theta)$ by searching for $\psi$ with stochastic gradient ascent. The gradient steps are taken with the estimator: **\ref{SalimansNES}**

$$\nabla_\psi E_{\theta \sim p_\psi} F(\theta)=E_{\theta \sim p_\psi} \{F(\theta)~\nabla_\psi~log~p_\psi(\theta)\}$$

In a Reinforcement Learning (RL) problem, F is the stochastic score returned by our environment (the Earth-Mars-Sun system) with $\theta$ representing the policy of an agent in the environment ($\Delta v$ for our spacecraft's path) and $\psi$ being the parametrization of that policy (launch parameters: angle, velocity, launch-time). The algorithm mutates the hyperparameters $\psi$, checks how the resulting path $\theta$ performs in the environment $F$ and moves around the resulting n-dimensional optimization space with gradient descent along its estimated gradient (we experiment with different dimensionalities for $\psi$, more on that later).
