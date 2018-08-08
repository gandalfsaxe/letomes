import time

from orbsim.r3b_2d import unit_velocity
from orbsim.plotting import orbitplot2d, orbitplot_non_inertial
from orbsim.r3b_2d.simulators import launch_sim

if __name__ == "__main__":
    # for x in range(10):
    #     psi = [rand() *2*pi, rand() * 2* pi, rand() * 4 / unit_velocity]
    #     path = launch_sim(psi)
    #     orbitplot2d(path, psi)
    # starttime=time.time()
    # psi = [-2.282942228154665, 0.0000, -31.49483130653266 / unit_velocity]
    # launch_sim(psi,max_iter=1000000)
    # print(round(time.time() - starttime, 3))

    starttime = time.time()
    # hohmann
    psi = [
        -2.086814820119193,
        -0.000122173047640,
        3.111181716545691 / unit_velocity,
    ]
    path = launch_sim(psi,max_iter=1e6)
    orbitplot2d(path, psi, title="hohmann")
    orbitplot_non_inertial(path, psi, title="hohmann")

    # reverse hohmann
    psi = [
        -2.282942228154665,
        0.000000000000000,
        -3.149483130653266 / unit_velocity,
    ]
    path = launch_sim(psi,max_iter=1e6)
    orbitplot2d(path, psi, title="reverse hohmann")
    orbitplot_non_inertial(path, psi, title="reverse_hohmann")

    # low energy long
    psi = [3.794182930145708, 0.023901745288554, 3.090702702702703 / unit_velocity]
    path = launch_sim(psi,max_iter=1e6)
    orbitplot2d(path, psi, title="LE long")
    orbitplot_non_inertial(path, psi, title="LE long")

    # low energy short
    psi = [
        -0.138042744751570,
        -0.144259374836607,
        3.127288444444444 / unit_velocity,
    ]
    path = launch_sim(psi,max_iter=1e6)
    orbitplot2d(path, psi, title="LE short")
    orbitplot_non_inertial(path, psi, title="LE short")

    # 3-day-hohmann
    psi = [
        -2.272183066647597,
        -0.075821466029764,
        3.135519748743719 / unit_velocity,
    ]
    path = launch_sim(psi,max_iter=1e6)
    orbitplot2d(path, psi, title="3-day-hohmann")
    orbitplot_non_inertial(path, psi, title="3-day-hohmann")

    # 1-day-hohmann
    psi = [-2.277654673852600, 0.047996554429844, 3.810000000000000 / unit_velocity]
    path = launch_sim(psi)
    orbitplot2d(path, psi, title="1-day-hohmann")
    orbitplot_non_inertial(path, psi, title="1-day-hohmann")

    print(round(time.time() - starttime, 3))
