---
bibliography: ../Slingshooters.bib
header-includes:
- \usepackage{siunitx}
---
# Introduction

This MSc Thesis is based on the BSc thesis "Low Energy Transfer Orbits - A Theoretical and Numerical Study" [@Saxe2015], where we aimed to find low energy transfer orbits (LETOs) to the moon. Part of the aim of the B.Sc. thesis was to show that finding LETOs was possible for a simplified restricted 3-body model (R3B) where it was possible to do everything manually, from the ground up; all the analytical mechanics could be worked out by hand and the equations of motion be nondimensionalized to a form that was practical to solve in a computer program. Likewise an acceptable numerical integration program could be implemented from the ground up in Python, with no use of external libraries. Another aim was to accelerate the simulations with GPUs such that good low delta-v LETOs could be found simply from brute force search.

## B.Sc. thesis results

We performed a Hohmann transfer orbit to the moon and compared flight time and delta-v with known values form the Apollo program, which agreed within 2.5%.

**INSERT HOHMANN TRANSFER FIGURE HERE.

This at least partly validated our simplified R3B sun-less model and numerical techniques. For the numerical integration we performed a second-order symplectic Störmer-Verlet that was made adaptive by **WAITING FOR HH TO RE-WRITE SECTION ON THIS.

**INSERT SV-ADAPTIVE STEPSIZE/ERROR HERE

By brute force searching in many directions and velocity vectors in a $\SI{100}{\km}$ parking orbit

## Aim of this thesis

The aim of this MSc thesis is to take in work of [@Saxe2015] further in several ways:

- We will now search the for LETOs using evolutionary techniques instead of random. Incidentally a paper [@Izzo2018] was published on this exact topic after we started work on this thesis, so it appears to be an idea ripe for exploration.
- We will now attempt LETOs to Mars in addition to the Moon.
- We will now work with a more realistic model instead of the R3B model. Now that we're doing interplanetary transfers, we will work with patched conic approximations on the analytical side and external libraries on the software side.
