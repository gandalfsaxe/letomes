import numpy as np
from numba import jit
from .constants import *
from .integrators import symplectic
from pykep.planet import jpl_lp
from pykep import epoch
import time

def launch_sim(psi, max_iter=1000000):
    """
    return: [Dv, [x, y, px, py, h]]
    launch (not really a launch since we start from LEO) a 
    single rocket with a given set of hyperparameters, return the resulting path
    """
    starttime=time.time()
    pos_ang, burn_ang, burnDv = psi  # extract parameters from decision vector

    """define init params"""
    # position (where on earth do we start our burn)
    x0 = np.cos(pos_ang) * leo_radius_nondim
    y0 = np.sin(pos_ang) * leo_radius_nondim
    x0 += earth_position_x

    # how fast are we going when we start?
    vhat_x = -np.sin(pos_ang)
    vhat_y = np.cos(pos_ang)
    v_x = (leo_velocity_nondim) * vhat_x
    v_y = (leo_velocity_nondim) * vhat_y

    # burn vector: At what angle do we launch outward, and how hard do we push?
    burnDv_x = np.cos(burn_ang) * vhat_x - np.sin(burn_ang) * vhat_y
    burnDv_y = np.sin(burn_ang) * vhat_x + np.cos(burn_ang) * vhat_y

    # resultant momentum vector
    p0_x = v_x + burnDv * burnDv_y - y0
    p0_y = v_y + burnDv * burnDv_x + x0

    """SIMULATE"""
    launch_sim_time=time.time()-starttime
    starttime = time.time()
    result = symplectic(x0, y0, p0_x, p0_y, max_iter=max_iter)
    symplectic_time=time.time()-starttime
    print(f"launch_sim: {launch_sim_time} \nsymplectic: {symplectic_time}")
    return result

class space:
    def __init__(self):
        self.mars = jpl_lp('mars')
        self.earth = jpl_lp('earth')

def net_gravitational_force(epoch, position):
    pass
    
