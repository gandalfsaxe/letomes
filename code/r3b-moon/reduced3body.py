"""
Reduced 3-Body Problem Solver Module
====================================
A collection of various numerical solvers for the reduced 3-body problem consisting of two larger masses (Earth, Moon) and one smaller moving in their gravitaional field (a satellite). The solution assumes Earth-Moon center of mass as origin and a cartesian x-y coordinate system rotating with the lines connecting the Earth and Moon (non-interial frame accounted for in the equations of motion).

Functions:

We assume **TODO FILL OUT HERE!

"""

import time
from math import pi,sqrt
import numpy as np
from const import *
from numbapro import *
from search import search_mt, search, print_search_results
from symplectic import symplectic

# **BRUGER IKKE pos, ang, burn til noget, kun til print
def trajectory(n,duration,pos,ang,burn,x0,y0,px0,py0):
    """Integrate trajectory for the reduced 3-body problem.

    Args:
        n (int): Positions stored.
        duration (float): Time duration of simulation.
        x0 (float): Initial x-coordinate
        y0 (float): Initial y-coordinate
        px0 (float): Initial generalized x-momentum
        py0 (float): Initial generalized y-momentum

    Returns:
        Tuple of time-, x-, y-, px- and py lists.
    
    """
    print("# Running trajectory.")

    # Initialize arrays
    tlist = np.linspace(0,duration,n)
    xlist = np.zeros(n)
    ylist = np.zeros(n)
    pxlist = np.zeros(n)
    pylist = np.zeros(n)
    errlist = np.zeros(n)
    hlist = np.zeros(n)
    info = np.zeros(2)

    # Find orbits
    runtime = time.time()
    status = symplectic(n,duration,x0,y0,px0,py0,xlist,ylist,pxlist,pylist,errlist,hlist,info)
    runtime = time.time()-runtime

    # Display result
    print_search_results(status,pos,ang,burn,x0,y0,px0,py0,info[0],info[1])
    print("# Runtime = %3.2fs" % (runtime))
    return tlist,xlist,ylist,pxlist,pylist,errlist,hlist

def hohmann(threads,n):
    """Finding Hohmann trajectory for the reduced 3-body problem.

    Args:
        n (int): Positions stored.

    Returns:
        Tuple of time-, x-, y-, px- and py lists.
    
    """

    print("# Running Hohmann.")

    # Hohmann trajectory < 6 days
    duration = 6/unit_time
    best_total_dv = 1e9
    positions = 100
    angles = 1
    burns = 200
    pos = -3*pi/4
    ang = 0
    burn = 3.11/unit_vel # Forward Hohmann
    #burn_low = -3.14/unit_vel # Reverse Hohmann

    # Super fast Hohmann trajectory < 1 days
    #duration = 3/unit_time
    #best_total_dv = 1e9
    #positions = 10
    #angles = 10
    #burns = 200
    #pos = -3*pi/4
    #ang = 0
    #burn = 3.7/unit_vel # Forward Hohmann

    pos_range = pi/4
    ang_range = pi/8
    burn_range = 0.1/unit_vel

    # Start search
    searches = 0
    max_searches = 5
    while searches < max_searches:
        runtime = time.time()
        searches += 1
        print("############## Search %i ###############" % (searches))
        print("# pos              = %f" % (pos))
        print("# ang              = %f" % (ang))
        print("# burn             = %f" % (burn))
        pos_low = pos-pos_range
        pos_high = pos+pos_range
        ang_low = ang-ang_range
        ang_high = ang+ang_range
        burn_low = burn-burn_range
        burn_high = burn+burn_range
        stat,pos,ang,burn,x0,y0,px0,py0,dv,toa = search_mt(threads,1,duration,positions,angles,burns,pos_low,pos_high,ang_low,ang_high,burn_low,burn_high)

        if stat < 0:
            total_dv = abs(burn)+dv
            if best_total_dv > total_dv:
                best_total_dv = total_dv
                best_stat = stat
                best_pos = pos
                best_ang = ang
                best_burn = burn
                best_x0 = x0
                best_y0 = y0
                best_px0 = px0
                best_py0 = py0
                best_dv = dv
                best_toa = toa
            else:
                break

        pos_range *= 0.1
        ang_range *= 0.1
        burn_range *= 0.1

        runtime = time.time()-runtime
        print("# Search runtime   = %3.2fs" % (runtime))

    # Print best result
    print("################ Best ################")
    print("# Best dV(total)   = %f km/s" % (best_total_dv*unit_vel))
    print_search_results(best_stat,best_pos,best_ang,best_burn,best_x0,best_y0,best_px0,best_py0,best_dv,best_toa)

    # Initialize arrays
    tlist = np.linspace(0,duration,n)
    xlist = np.zeros(n)
    ylist = np.zeros(n)
    pxlist = np.zeros(n)
    pylist = np.zeros(n)
    errlist = np.zeros(n)
    hlist = np.zeros(n)
    info = np.zeros(2)

    # Do trajectory
    duration = 10/unit_time
    status = symplectic(n,duration,x0,y0,px0,py0,xlist,ylist,pxlist,pylist,errlist,hlist,info)

    return tlist,xlist,ylist,pxlist,pylist,errlist,hlist

def low_energy(threads,n):
    """Finding low energy transfer trajectory for the reduced 3-body problem.

    Args:
        n (int): Positions stored.

    Returns:
        Tuple of time-, x-, y-, px- and py lists.
    
    """

    print("# Running low_energy.")

    # Low-energy trajectory < 200 days
    duration = 200/unit_time
    best_total_dv = 1e9
    positions = 100
    angles = 1
    burns = 200
    pos = -3*pi/4
    ang = 0
    burn = 3.12/unit_vel
    pos_range = pi
    ang_range = 0
    burn_range = 0.01/unit_vel

    # Start search
    searches = 0
    max_searches = 1
    while searches < max_searches:
        runtime = time.time()
        searches += 1
        print("############## Search %i ###############" % (searches))
        print("# pos              = %f" % (pos))
        print("# ang              = %f" % (ang))
        print("# burn             = %f" % (burn))
        pos_low = pos-pos_range
        pos_high = pos+pos_range
        ang_low = ang-ang_range
        ang_high = ang+ang_range
        burn_low = burn-burn_range
        burn_high = burn+burn_range
        stat,pos,ang,burn,x0,y0,px0,py0,dv,toa = search_mt(threads,1,duration,positions,angles,burns,pos_low,pos_high,ang_low,ang_high,burn_low,burn_high)

        if stat < 0:
            total_dv = abs(burn)+dv
            if best_total_dv > total_dv:
                best_total_dv = total_dv
                best_stat = stat
                best_pos = pos
                best_ang = ang
                best_burn = burn
                best_x0 = x0
                best_y0 = y0
                best_px0 = px0
                best_py0 = py0
                best_dv = dv
                best_toa = toa
            else:
                break

        pos_range *= 0.1
        ang_range *= 0.1
        burn_range *= 0.1

        runtime = time.time()-runtime
        print("# Search runtime   = %3.2fs" % (runtime))

    # Initialize arrays
    tlist = np.linspace(0,duration,n)
    xlist = np.zeros(n)
    ylist = np.zeros(n)
    pxlist = np.zeros(n)
    pylist = np.zeros(n)
    errlist = np.zeros(n)
    hlist = np.zeros(n)
    info = np.zeros(2)

    # Do trajectory
    duration = toa+(2.0*pi*lunar_orbit/lunar_orbit_vel)/(unit_time*day)
    status = symplectic(n,duration,x0,y0,px0,py0,xlist,ylist,pxlist,pylist,errlist,hlist,info)
    exit()
    return tlist,xlist,ylist,pxlist,pylist,errlist,hlist

def low_energy_parts8(threads,n):
    """Finding low energy transfer trajectory for the reduced 3-body problem.

    Args:
        n (int): Positions stored.

    Returns:
        Tuple of time-, x-, y-, px- and py lists.
    
    """

    print("# Running low_energy_parts8.")

    # Low-energy-short trajectory < 47 days
    duration = 200/unit_time
    best_total_dv = 1e9
    best_toa = 0
    positions = 55
    angles = 1
    burns = 55

    # Divide circular earth orbit into 8 parts
    for i in range(0,8):
        pos = i*pi/4
        ang = 0
        #burn = 3.12/unit_vel # moon
        burn = 3.09/unit_vel # L1
        pos_range = 2*pi/16
        ang_range = pi/2
        burn_range = 0.1/unit_vel
    
        # Start search
        searches = 0
        max_searches = 3
        while searches < max_searches:
            runtime = time.time()
            searches += 1
            print("############## Search %i ###############" % (searches))
            print("# pos              = %f" % (pos))
            print("# ang              = %f" % (ang))
            print("# burn             = %f" % (burn))
            pos_low = pos-pos_range
            pos_high = pos+pos_range
            ang_low = ang-ang_range
            ang_high = ang+ang_range
            burn_low = burn-burn_range
            burn_high = burn+burn_range
            stat,pos,ang,burn,x0,y0,px0,py0,dv,toa = search_mt(threads,1,duration,positions,angles,burns,pos_low,pos_high,ang_low,ang_high,burn_low,burn_high)

            if stat < 0:
                total_dv = abs(burn)+dv
                if best_total_dv > total_dv:
                    best_total_dv = total_dv
                    best_stat = stat
                    best_pos = pos
                    best_ang = ang
                    best_burn = burn
                    best_x0 = x0
                    best_y0 = y0
                    best_px0 = px0
                    best_py0 = py0
                    best_dv = dv
                    best_toa = toa
                else:
                    break

            pos_range *= 0.1
            ang_range *= 0.1
            burn_range *= 0.1

            runtime = time.time()-runtime
            print("# Search runtime   = %3.2fs" % (runtime))

    # Print best result
    if best_total_dv < 1e9:
        print("################ Best ################")
        print("# Best dV(total)   = %f km/s" % (best_total_dv*unit_vel))
        print_search_results(best_stat,best_pos,best_ang,best_burn,best_x0,best_y0,best_px0,best_py0,best_dv,best_toa)

    # Initialize arrays
    tlist = np.linspace(0,duration,n)
    xlist = np.zeros(n)
    ylist = np.zeros(n)
    pxlist = np.zeros(n)
    pylist = np.zeros(n)
    errlist = np.zeros(n)
    hlist = np.zeros(n)
    info = np.zeros(2)

    # Do trajectory
    #duration = toa+(2.0*pi*lunar_orbit/lunar_orbit_vel)/(unit_time*day)
    status = symplectic(n,duration,x0,y0,px0,py0,xlist,ylist,pxlist,pylist,errlist,hlist,info)
    #exit()
    return tlist,xlist,ylist,pxlist,pylist,errlist,hlist


def refine(threads,n,duration,pos,ang,burn,x0,y0,px0,py0):
    """Integrate trajectory for the reduced 3-body problem.

    Args:
        n (int): Positions stored.
        duration (float): Time duration of simulation.
        x0 (float): Initial x-coordinate
        y0 (float): Initial y-coordinate
        px0 (float): Initial generalized x-momentum
        py0 (float): Initial generalized y-momentum

    Returns:
        Tuple of time-, x-, y-, px- and py lists.
    
    """
    print("# Running refine.")

    # Low-energy-long trajectory < 200 days
    #duration = 200/unit_time
    # Low-energy-short trajectory < 47 days
    #duration = 47/unit_time
    best_total_dv = 1e9
    best_toa = 0
    positions = 15
    angles = 15
    burns = 15

    # Divide circular earth orbit into 8 parts
    pos_range = 2*pi/16*0.1
    ang_range = pi/100*0.1
    burn_range = 0.1/unit_vel*0.1
    
    # Start search
    searches = 0
    max_searches = 10
    while searches < max_searches:
        runtime = time.time()
        searches += 1
        print("############## Search %i ###############" % (searches))
        print("# pos              = %f" % (pos))
        print("# ang              = %f" % (ang))
        print("# burn             = %f" % (burn))
        pos_low = pos-pos_range
        pos_high = pos+pos_range
        ang_low = ang-ang_range
        ang_high = ang+ang_range
        burn_low = burn-burn_range
        burn_high = burn+burn_range
        stat,pos,ang,burn,x0,y0,px0,py0,dv,toa = search_mt(threads,1,duration,positions,angles,burns,pos_low,pos_high,ang_low,ang_high,burn_low,burn_high)

        if stat < 0:
            total_dv = abs(burn)+dv
            if best_total_dv > total_dv:
                best_total_dv = total_dv
                best_stat = stat
                best_pos = pos
                best_ang = ang
                best_burn = burn
                best_x0 = x0
                best_y0 = y0
                best_px0 = px0
                best_py0 = py0
                best_dv = dv
                best_toa = toa
            else:
                break
            
        pos_range *= 0.1
        ang_range *= 0.1
        burn_range *= 0.1

        runtime = time.time()-runtime
        print("# Search runtime   = %3.2fs" % (runtime))

    # Print best result
    print("################ Best ################")
    print("# Best dV(total)   = %f km/s" % (best_total_dv*unit_vel))
    print_search_results(best_stat,best_pos,best_ang,best_burn,best_x0,best_y0,best_px0,best_py0,best_dv,best_toa)

    # Initialize arrays
    tlist = np.linspace(0,duration,n)
    xlist = np.zeros(n)
    ylist = np.zeros(n)
    pxlist = np.zeros(n)
    pylist = np.zeros(n)
    errlist = np.zeros(n)
    hlist = np.zeros(n)
    info = np.zeros(2)

    # Do trajectory
    duration = toa+(2.0*pi*lunar_orbit/lunar_orbit_vel)/(unit_time*day)
    status = symplectic(n,duration,x0,y0,px0,py0,xlist,ylist,pxlist,pylist,errlist,hlist,info)
    #exit()
    return tlist,xlist,ylist,pxlist,pylist,errlist,hlist
