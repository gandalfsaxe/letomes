# The Orbsim Module

We have arranged our code into a python module that offers us some nice modularity and extensibility, at least as far as our relatively specific problem is concerned. What follows is an explanation of the architecture of this module.

## Abstractions

The simulator is a numerical solver for an analytical problem, implementing algorithms that have been defined through that analysis. Thus, we have taken care to keep nomenclature consistent between the simulator and its analytical foundations. Between code and paper, if you will. This is complicated somewhat by the fact that we are applying Evolution Strategies as our search strategy, which carries with it its own set of nomenclature from the machine learning world. We have kept the two things largely separate, with the ES module interacting with the simulator through a relatively simple interface. This works fine, since ES is a black-box optimizer anyway.

## Simulator module

Here, we have the interface between ES portion and simulator. The function **launch_sim** takes hyperparameters that the ES algorithm uses for its optimization (in the form of a decision vector $\psi$), reformulates them, and starts a simulation based on them. It then returns a $\Delta v$ for that single run, along with the associated saved path. That $\Delta v$ is, as mentioned before, our fitness function, so based on that result, ES can continue to do its job.

## Integrators module

This contains the main loop of our simulator algorithm, along with subfunctions for the individual steps.

## Analyticals module

This module contains a ton of different convenience functions that compute some intermediate equation for use in the main algorithm. They are hidden away here to reduce clutter in **integrators**.

## Planets module

Here, we define a planet class, which we use to store the various constants associated with a given planet. Note that we also consider the moon a planet for this purpose. We keep information such as mass and safe orbital radius here, again to simplify and improve the readability of the main algorithm. The full list of planetary constants can be seen in \ref{planetaryConstants}