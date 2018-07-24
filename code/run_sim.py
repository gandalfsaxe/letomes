from orbsim.constants import *
from orbsim.plotting import orbitplot
from orbsim.simulators import launch_sim

if __name__ == "__main__":
    path = launch_sim([2.87, 0.12, 1.1111 / unit_velocity])

    orbitplot(path)
