"""
Reduced 3-body Problem testing script
====================================
Testing the reduced 3-body problem solvers with different numerical algorithms.

"""
import os
import sys
import time
from math import cos, pi, sin

import matplotlib.pyplot as plt
import numpy as np

from r3b_numba import reduced3body as r3b
from orbsim.constants import *


def run_test():

    old_stdout = sys.stdout
    log_file = open("r3b-refactor.log","w")
    sys.stdout = log_file

    try:  
        threads = int(os.environ["OMP_NUM_THREADS"])
    except KeyError: 
        threads = 1

    runtime = time.time()

    FORMAT = "png"
    # FORMAT = "pdf"

    ### Precalculated initial Conditions
    # DEMO = 'closed_earth_orbit'
    # DEMO = 'closed_lunar_orbit'
    # DEMO = 'hohmann'
    # DEMO = '3_day_hohmann'
    # DEMO = '1_day_hohmann'
    # DEMO = 'reverse_hohmann'
    # DEMO = 'low_energy_short'
    # DEMO = 'low_energy_long'
    # DEMO = 'earth_to_L1'

    ### Or search for trajectories
    DEMO = 'search_hohmann'
    # DEMO = 'search_low_energy'
    # DEMO = 'search_low_energy_parts8'
    # DEMO = 'search_refine'

    n = 1000000

    # Set coordinates
    if DEMO == 'closed_earth_orbit':
        duration = (2.0*pi*leo_radius/leo_velocity)/(unit_time*day)
        r = leo_radius/unit_length
        v = 0.99732*leo_velocity/unit_velocity
        theta = 0
        x = r*cos(theta)
        y = r*sin(theta)
        vx = -v*y/r
        vy = v*x/r
        pos = 0
        ang = 0
        burn = 0
        x0 = earth_pos_x+x
        y0 = y
        px0 = vx-y0
        py0 = vy+x0
    elif DEMO == 'closed_lunar_orbit':
        duration = (2.0*pi*llo_radius/llo_velocity)/(unit_time*day)
        r = llo_radius/unit_length
        v = 0.99732*llo_velocity/unit_velocity
        theta = 0
        x = r*cos(theta)
        y = r*sin(theta)
        vx = -v*y/r
        vy = v*x/r
        pos = 0
        ang = 0
        burn = 0
        x0 = moon_position_X+x
        y0 = y
        px0 = vx-y0
        py0 = vy+x0
    elif DEMO == 'hohmann':
        #DEMO = 'search_refine'
    # --------------------------------------------------------------------------
        duration = 5/unit_time
        pos      = -2.086814820119193
        ang      = -0.000122173047640
        burn     = 3.111181716545691/unit_velocity
        x0       = -0.020532317163607
        y0       = -0.014769797663479
        px0      = 9.302400979050308
        py0      = -5.289712560652044
    # --------------------------------------------------------------------------
    # dV(earth-escape) = 3.111182 km/s
    # dV(moon-capture) = 0.800682 km/s
    # dV(total)        = 3.911863 km/s
    # Flight-time      = 4.300078 days
    # --------------------------------------------------------------------------
    elif DEMO == 'reverse_hohmann':
    # --------------------------------------------------------------------------
        duration = 4/unit_time
        pos      = -2.282942228154665
        ang      = 0.000000000000000
        burn     = -3.149483130653266/unit_velocity
        x0       = -0.023249912090507
        y0       = -0.012853859046429
        px0      = -8.098481905534163
        py0      = 6.978997254692934
    # --------------------------------------------------------------------------
    # dV(earth-escape) = 3.149483 km/s
    # dV(moon-capture) = 0.968488 km/s
    # dV(total)        = 4.117971 km/s
    # Flight-time      = 3.875497 days
    # --------------------------------------------------------------------------
    elif DEMO == 'low_energy_long':
    # --------------------------------------------------------------------------
        duration = 195/unit_time
        pos      = 3.794182930145708
        ang      = 0.023901745288554
        burn     = 3.090702702702703/unit_velocity
        x0       = -0.025645129237870
        y0       = -0.010311570301966
        px0      = 6.539303578815582
        py0      = -8.449205705334165
    # --------------------------------------------------------------------------
    # dV(earth-escape) = 3.090703 km/s
    # dV(moon-capture) = 0.704114 km/s
    # dV(total)        = 3.794816 km/s
    # Flight-time      = 194.275480 days
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
        #DEMO = 'search_refine'
    #    duration = 195/unit_time
    #    pos      = 3.794182930145708
    #    ang      = 0.023901745288554
    #    burn     = 3.090702702702703/unit_velocity
    #    x0       = -0.025645129237870
    #    y0       = -0.010311570301966
    #    px0      = 6.539303578815583
    #    py0      = -8.449205705334164
    # --------------------------------------------------------------------------
    # dV(earth-escape) = 3.090703 km/s
    # dV(moon-capture) = 0.704114 km/s
    # dV(total)        = 3.794817 km/s
    # Flight-time      = 194.275480 days
    # --------------------------------------------------------------------------
    elif DEMO == 'low_energy_short':
        #DEMO = 'search_refine'
    # --------------------------------------------------------------------------
        duration = 41/unit_time
        pos      = -0.138042744751570
        ang      = -0.144259374836607
        burn     = 3.127288444444444/unit_velocity
        x0       = 0.004665728429046
        y0       = -0.002336647636098
        px0      = 1.904735175752430
        py0      = 10.504985512873279
    # --------------------------------------------------------------------------
    # dV(earth-escape) = 3.127288 km/s
    # dV(moon-capture) = 0.768534 km/s
    # dV(total)        = 3.895822 km/s
    # Flight-time      = 40.617871 days
    # --------------------------------------------------------------------------
    elif DEMO == '3_day_hohmann':
        #DEMO = 'search_refine'
    # --------------------------------------------------------------------------
        duration = 3/unit_time
        pos      = -2.272183066647597
        ang      = -0.075821466029764
        burn     = 3.135519748743719/unit_velocity
        x0       = -0.023110975767437
        y0       = -0.012972499765730
        px0      = 8.032228991913522
        py0      = -7.100537706154897
    # --------------------------------------------------------------------------
    # dV(earth-escape) = 3.135520 km/s
    # dV(moon-capture) = 0.879826 km/s
    # dV(total)        = 4.015346 km/s
    # Flight-time      = 2.999939 days
    # --------------------------------------------------------------------------
    elif DEMO == '1_day_hohmann':
        #DEMO = 'search_refine'
        duration = 1/unit_time
        pos      = -2.277654673852600
        ang      = 0.047996554429844
        burn     = 3.810000000000000/unit_velocity
        x0       = -0.023181791813268
        y0       = -0.012912351430812
        px0      = 8.764829132987316
        py0      = -7.263069305305378
    # --------------------------------------------------------------------------
    # dV(earth-escape) = 3.810000 km/s
    # dV(moon-capture) = 3.319455 km/s
    # dV(total)        = 7.129455 km/s
    # Flight-time      = 0.997234 days
    # --------------------------------------------------------------------------
    elif DEMO == 'earth_to_L1':
        DEMO = 'search_refine'
    # --------------------------------------------------------------------------
        duration = 191/unit_time
        pos      = 2.843432239707429
        ang      = 0.000000000000000
        burn     = 3.091851851851852/unit_velocity
        x0       = -0.028385246222264
        y0       = 0.004988337832881
        px0      = -3.136296304910217
        py0      = -10.217405925499762
    # --------------------------------------------------------------------------
    # dV(earth-escape) = 3.091852 km/s
    # dV(at L1)        = 0.676226 km/s
    # dV(total)        = 3.768078 km/s
    # Flight-time      = 190.001881 days
    # --------------------------------------------------------------------------

    #################### FUNCTION CALLS ####################

    if DEMO == 'search_hohmann':
        tlist,xlist,ylist,pxlist,pylist,errlist,hlist = r3b.hohmann(threads,n)
    elif DEMO == 'search_low_energy':
        tlist,xlist,ylist,pxlist,pylist,errlist,hlist = r3b.low_energy(threads,n)
    elif DEMO == 'search_low_energy_parts8':
        tlist,xlist,ylist,pxlist,pylist,errlist,hlist = r3b.low_energy_parts8(threads,n)
    elif DEMO == 'search_refine':
        tlist,xlist,ylist,pxlist,pylist,errlist,hlist = r3b.refine(threads,n,duration,pos,ang,burn,x0,y0,px0,py0)
    else:
        tlist,xlist,ylist,pxlist,pylist,errlist,hlist = r3b.trajectory(n,duration,pos,ang,burn,x0,y0,px0,py0)
    Hlist = pxlist**2/2 + pylist**2/2 + ylist*pxlist - xlist*pylist - (1-mu)/np.sqrt(np.power(mu+xlist,2)+np.power(ylist,2)) - mu/np.sqrt(np.power(1-mu-xlist,2)+np.power(ylist,2))
    print("# Final position: %f %f" %(xlist[n-1],ylist[n-1]))
    print("# Final impulse: %f %f" % (pxlist[n-1],pylist[n-1]))
    print("# Final H: %f" % (Hlist[n-1]))
    runtime = time.time()-runtime
    print("# Total runtime = %3.2fs" % (runtime))
    print("# --------------------------------------------------------------------------")
    print("# --- Done with FUNCTION CALLS")
    #exit()

    #################### PLOTS: POSITION ####################

    n2 = int(n/2)

    xlist1 = xlist[:n2]
    ylist1 = ylist[:n2]
    xlist2 = xlist[n2:]
    ylist2 = ylist[n2:]

    Xlist1 = xlist[:n2]*np.cos(tlist[:n2]) - ylist[:n2]*np.sin(tlist[:n2])
    Ylist1 = xlist[:n2]*np.sin(tlist[:n2]) + ylist[:n2]*np.cos(tlist[:n2])
    Xlist2 = xlist[n2:]*np.cos(tlist[n2:]) - ylist[n2:]*np.sin(tlist[n2:])
    Ylist2 = xlist[n2:]*np.sin(tlist[n2:]) + ylist[n2:]*np.cos(tlist[n2:])

    Xlist_earth = earth_pos_x*np.cos(tlist)
    Ylist_earth = -earth_pos_x*np.sin(tlist)

    Xlist_moon = moon_position_X*np.cos(tlist)
    Ylist_moon = moon_position_X*np.sin(tlist)

    # Rel. err
    plt.figure()
    plt.plot(tlist*unit_time, errlist)
    plt.xlabel("time (days)")
    plt.ylabel("step error")
    plt.yscale('log')
    plt.savefig('r3b-moon/fig/{}-step_error_vs_time.{}'.format(DEMO, FORMAT),bbox_inches='tight')

    # Step sizes
    plt.figure()
    plt.plot(tlist*unit_time, hlist)
    plt.xlabel("time (days)")
    plt.ylabel("step size")
    plt.yscale('log')
    plt.savefig('r3b-moon/fig/{}-step_size_vs_time.{}'.format(DEMO, FORMAT),bbox_inches='tight')

    # Total energy error
    havg = np.sum(Hlist)/n
    hrelerr = (Hlist-havg)/havg
    plt.figure()
    plt.plot(tlist*unit_time, hrelerr)
    plt.xlabel("time (days)")
    plt.ylabel("Hamiltonian rel. err (arbitrary units)")
    plt.savefig('r3b-moon/fig/{}-energy_error_vs_time.{}'.format(DEMO, FORMAT),bbox_inches='tight')

    # Zoom earth
    xlim = 0.02
    ylim = 0.02
    xmin = earth_pos_x-xlim
    xmax = earth_pos_x+xlim
    ymin = -ylim
    ymax = ylim
    plt.figure()
    earth=plt.Circle((earth_pos_x,0),earth_radius/unit_length,color='blue')
    earthorbit1=plt.Circle((earth_pos_x,0),(leo_radius-ORBITAL_TOLERANCE)/unit_length,color='g',fill=False)
    earthorbit2=plt.Circle((earth_pos_x,0),(leo_radius+ORBITAL_TOLERANCE)/unit_length,color='g',fill=False)
    plt.gcf().gca().add_artist(earth)
    plt.gcf().gca().add_artist(earthorbit1)
    plt.gcf().gca().add_artist(earthorbit2)
    plt.plot(xlist1,ylist1,'r-')
    plt.plot(xlist2,ylist2,'k-')
    plt.xlim(xmin,xmax)
    plt.ylim(ymin,ymax)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlabel("x-position (arbitrary units)")
    plt.ylabel("y-position (arbitrary units)")
    plt.savefig('r3b-moon/fig/{}-earth_exit_y(x).{}'.format(DEMO, FORMAT),bbox_inches='tight')

    # Zoom moon
    xlim = 0.0055
    ylim = 0.0055
    xmin = moon_position_X-xlim
    xmax = moon_position_X+xlim
    ymin = -ylim
    ymax = ylim
    plt.figure()
    moon=plt.Circle((moon_position_X,0),lunar_radius/unit_length,color='grey')
    moonorbit1=plt.Circle((moon_position_X,0),(llo_radius-ORBITAL_TOLERANCE)/unit_length,color='g',fill=False)
    moonorbit2=plt.Circle((moon_position_X,0),(llo_radius+ORBITAL_TOLERANCE)/unit_length,color='g',fill=False)
    plt.gcf().gca().add_artist(moon)
    plt.gcf().gca().add_artist(moonorbit1)
    plt.gcf().gca().add_artist(moonorbit2)
    plt.plot(xlist1,ylist1,'r-')
    plt.plot(xlist2,ylist2,'k-')
    plt.xlim(xmin,xmax)
    plt.ylim(ymin,ymax)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlabel("x-position (arbitrary units)")
    plt.ylabel("y-position (arbitrary units)")
    plt.savefig('r3b-moon/fig/{}-moon_entry_y(x).{}'.format(DEMO, FORMAT),bbox_inches='tight')

    # View center of mass
    xlim = 1.3
    ylim = 1.3
    xmin = -xlim
    xmax = xlim
    ymin = -ylim
    ymax = ylim

    # Position plot (X,Y)
    plt.figure()
    plt.plot(Xlist1,Ylist1,'r')
    plt.plot(Xlist2,Ylist2,'k')
    plt.plot(Xlist_earth, Ylist_earth, 'blue')
    plt.plot(Xlist_moon, Ylist_moon, 'grey')
    plt.xlim(xmin,xmax)
    plt.ylim(ymin,ymax)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlabel("x-position (arbitrary units)")
    plt.ylabel("y-position (arbitrary units)")
    plt.savefig('r3b-moon/fig/{}-Y(X)_inertial.{}'.format(DEMO, FORMAT),bbox_inches='tight')

    # Position plot (x,y)
    plt.figure()
    plt.plot(xlist1,ylist1,'r-')
    plt.plot(xlist2,ylist2,'k-')
    earth=plt.Circle((earth_pos_x,0),earth_radius/unit_length,color='blue')
    earthorbit1=plt.Circle((earth_pos_x,0),(leo_radius-ORBITAL_TOLERANCE)/unit_length,color='g',fill=False)
    earthorbit2=plt.Circle((earth_pos_x,0),(leo_radius+ORBITAL_TOLERANCE)/unit_length,color='g',fill=False)
    moon=plt.Circle((moon_position_X,0),lunar_radius/unit_length,color='grey')
    moonorbit1=plt.Circle((moon_position_X,0),(llo_radius-ORBITAL_TOLERANCE)/unit_length,color='g',fill=False)
    moonorbit2=plt.Circle((moon_position_X,0),(llo_radius+ORBITAL_TOLERANCE)/unit_length,color='g',fill=False)
    plt.gcf().gca().add_artist(earth)
    plt.gcf().gca().add_artist(earthorbit1)
    plt.gcf().gca().add_artist(earthorbit2)
    plt.gcf().gca().add_artist(moon)
    plt.gcf().gca().add_artist(moonorbit1)
    plt.gcf().gca().add_artist(moonorbit2)
    plt.plot(L1_position_x,0,'gx')
    plt.xlim(xmin,xmax)
    plt.ylim(ymin,ymax)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlabel("x-position (arbitrary units)")
    plt.ylabel("y-position (arbitrary units)")
    plt.savefig('r3b-moon/fig/{}-y(x)_corotating.{}'.format(DEMO, FORMAT),bbox_inches='tight')
    # plt.savefig('r3b/r3b_y(x)_euler_symplectic.{}',DEMO, FORMAT='tight')
    # plt.show()
    plt.close()
    print("# --- Done with PLOTS")

    # # #################### PLOTS: VELOCITY ####################

    # plt.figure()
    # plt.plot(tlist, omegalist_e)
    # plt.xlabel("time (arbitrary units)")
    # plt.ylabel("velocity (arbitrary units)")
    # plt.savefig('r3b/r3b_omega(t)_euler_explicit.{}')
    # # plt.DEMO, FORMATow()
    # plt.close()

    # #################### PHASE-SPACE TRAJECTORY PLOTS ####################

    # # Explicit Euler phase-space trajectory
    # plt.figure()
    # plt.plot(thetalist_e[:len(thetalist_e)/2], omegalist_e[:len(omegalist_e)/2], 'r')
    # plt.plot(thetalist_e[len(thetalist_e)/2:], omegalist_e[len(omegalist_e)/2:], 'b')
    # plt.xlabel("position (arbitrary units)")
    # plt.ylabel("velocity (arbitrary units)")
    # plt.savefig('r3b/r3b_phase-space_euler_explicit.{}',DEMO, FORMAT='tight')
    # #plt.show()
    # plt.close()

    # # Implicit Euler phase-space trajectory
    # plt.figure()
    # plt.plot(thetalist_i[:len(thetalist_i)/2], omegalist_i[:len(omegalist_i)/2], 'r')
    # plt.plot(thetalist_i[len(thetalist_i)/2:], omegalist_i[len(omegalist_i)/2:], 'b')
    # plt.xlabel("position (arbitrary units)")
    # plt.ylabel("velocity (arbitrary units)")
    # plt.savefig('r3b/r3b_phase-space_euler_implicit.{}',DEMO, FORMAT='tight')
    # #plt.show()
    # plt.close()

    # # Symplectic Euler phase-space trajectory
    # plt.figure()
    # plt.plot(thetalist[:len(thetalist)/2], omegalist[:len(omegalist)/2], 'r')
    # plt.plot(thetalist[len(thetalist)/2:], omegalist[len(omegalist)/2:], 'b')
    # plt.xlabel("position (arbitrary units)")
    # plt.ylabel("velocity (arbitrary units)")
    # plt.savefig('r3b/r3b_phase-space_euler_symplectic.{}',DEMO, FORMAT='tight')
    # #plt.show()
    # plt.close()

    # print("--- Done with PHASE-SPACE TRAJETORY PLOTS")

    sys.stdout = old_stdout
    log_file.close()
    
if __name__ == '__main__':
    run_test()