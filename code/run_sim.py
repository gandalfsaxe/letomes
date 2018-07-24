from orbsim.constants import *
from orbsim.plotting import orbitplot
from orbsim.simulators import launch_sim

if __name__ == "__main__":
    path = launch_sim([-2.087, -1.00012, 3.1111])
    orbitplot(path)
