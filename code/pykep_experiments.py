
# coding: utf-8

# In[ ]:
import sys
sys.path = [""] + sys.path

import pygmo as pg
from pykep import epoch, util
from pykep.planet import jpl_lp
from pykep.planet import spice
from pykep.trajopt import mga_1dsm

# In[ ]:


def goto_mars():
    # We define an Earth-Mars problem (single-objective)
    seq = [jpl_lp('earth'),jpl_lp('mars')]
    udp = mga_1dsm(
        seq=seq,
        t0=[epoch(18*365.25 + 1), epoch(25*365.25 + 1)],
        tof=[0.7 * 365.25, 7 * 365.25],
        vinf=[0.5, 5],
        add_vinf_dep=False,
        add_vinf_arr=True,
        multi_objective=False
    )

    pg.problem(udp)
    # We solve it!!
    uda = pg.sade(gen=200)
    archi = pg.archipelago(algo=uda, prob=udp, n=8, pop_size=30)
    print(
        "Running a Self-Adaptive Differential Evolution Algorithm .... on 8 parallel islands")
    archi.evolve(10)
    archi.wait()
    sols = archi.get_champions_f()
    idx = sols.index(min(sols))
    print("Done!! Solutions found are: ", archi.get_champions_f())
    print(f"\nThe best solution with Dv = {min(sols)[0]}:\n")
    udp.pretty(archi.get_champions_x()[idx])
    udp.plot(archi.get_champions_x()[idx])


# In[ ]:

if __name__ == "__main__":
    goto_mars()


