"""
Reduced 3-Body Problem Solver Module
====================================
A collection of various numerical solvers for the reduced 3-body problem consisting of two larger masses (Earth, Moon) and one smaller moving in their gravitaional field (a satellite). The solution assumes Earth-Moon center of mass as origin and a cartesian x-y coordinate system rotating with the lines connecting the Earth and Moon (non-interial frame accounted for in the equations of motion).

Functions:
    euler: Solves by Euler method explicitely, implicitely or symplectically.

We assume **TODO FILL OUT HERE!

"""

import math
import numpy as np
from numbapro import *

# Table constants
earth_moon_distance = 384400.0 # km
moon_orbit_duration = 27.322 # days
earth_radius = 6367.4447 # km
earth_mass = 5.9721986e24
moon_mass = 7.34767309e22
G = 6.67384e-11 # m^3 kg^-1 s^-2
moon_radius = 1737.1 # km
leo_orbit = 160.0+earth_radius # km
lunar_orbit = 100.0+moon_radius # km
orbit_range = 10.0 # km

# Units
unit_len = earth_moon_distance # km
unit_time = moon_orbit_duration/(2.0*np.pi) # days
unit_vel = unit_len/(unit_time*24.0*3600.0) # km/s

# Gravitational constants
mu = moon_mass/(earth_mass+moon_mass) # 1
mu_moon = 4902.8000 # km^3 s^-2
mu_earth = 398600.4418 # km^3 s^-2

# Calculation constants
moon_pos_x = 1-mu
earth_pos_x = -mu
earth_orbit_vel = math.sqrt(mu_earth/earth_radius)
moon_orbit_vel = math.sqrt(mu_moon/moon_radius)

@jit
def F(x,y):
    mux = mu+x
    mux2 = mux*mux
    mumx = 1-mux
    mumx2 = mumx*mumx
    y2 = y*y
    denum1 = 1.0/((mux2+y2)*math.sqrt(mux2+y2))
    denum2 = 1.0/((mumx2+y2)*math.sqrt(mumx2+y2))
    Fx = (mu-1.0)*mux*denum1+mu*mumx*denum2
    Fy = (mu-1.0)*y*denum1-mu*y*denum2
    return Fx,Fy

@jit
def explicit_euler_step(h,x,y,px,py):
    Fx,Fy = F(x,y)
    vx = px+y
    vy = py-x
    vpx = Fx+py
    vpy = Fy-px
    x += vx*h
    y += vy*h
    px += vpx*h
    py += vpy*h
    return x,y,px,py

@jit
def symplectic_euler_step(h,x,y,px,py):
    # Step 1
    vx = px+y
    x = (x+(vx+py*h)*h)/(1.0+h*h)
    vy = py-x
    y += vy*h
    # Step 2
    Fx,Fy = F(x,y)
    vpx = Fx+py
    vpy = Fy-px
    px += vpx*h
    py += vpy*h
    return x,y,px,py

@jit
def symplectic_euler_step1(h,x,y,px,py):
    # Step 1
    Fx,Fy = F(x,y)
    vpx = Fx+py
    px = (px+(vpx+Fy*h)*h)/(1.0+h*h)
    vpy = Fy-px
    py += vpy*h
    # Step 2
    vx = px+y
    vy = py-x
    x += vx*h
    y += vy*h
    return x,y,px,py

@jit
def symplectic_euler_step2(h,x,y,px,py):
    # Step 1
    Fx,Fy = F(x,y)
    vpx = Fx+py
    vpy = Fy-px
    px += vpx*h
    py += vpy*h
    # Step 2
    vx = px+y
    x = (x+(vx+py*h)*h)/(1.0+h*h)
    vy = py-x
    y += vy*h
    return x,y,px,py

@jit
def symplectic_verlet_step(h,x,y,px,py):
    hh = 0.5*h
    denum = 1.0/(1.0+hh*hh)
    # Step 1
    vx = px+y
    x = (x+(vx+py*hh)*hh)*denum
    vy = py-x
    y += vy*hh
    # Step 2
    Fx,Fy = F(x,y)
    vpx = Fx+py
    vpy = Fy-px
    px = (px+(2.0*vpx+(vpy+Fy)*hh)*hh)*denum
    py += (vpy+Fy-px)*hh
    # Step 3
    vx = px+y
    vy = py-x
    x += vx*hh
    y += vy*hh
    return x,y,px,py

@jit
def symplectic_verlet_step2(h,x,y,px,py):
    hh = 0.5*h
    denum = 1.0/(1.0+hh*hh)
    # Step 1
    Fx,Fy = F(x,y)
    vpx = Fx+py
    px = (px+(vpx+Fy*hh)*hh)*denum
    vpy = Fy-px
    py += vpy*hh
    # Step 2
    vx = px+y
    vy = py-x
    x = (x+(2.0*vx+(vy+py)*hh)*hh)*denum
    y += (vy+py-x)*hh
    # Step 3
    Fx,Fy = F(x,y)
    vpx = Fx+py
    vpy = Fy-px
    px += vpx*hh
    py += vpy*hh
    return x,y,px,py

@jit #('void(int64, float64, float64, float64, float64, float64, float64, float64[:], float64[:], float64[:], float64[:])')
def symplectic(n,duration,x0,y0,px0,py0,xlist,ylist,pxlist,pylist,errlist,hlist):

    # Initialize initial conditions
    h = 0.5e-6
    hmin = 1e-10
    hmax = 1e-3
    tol = 1e-9
    x = x0
    y = y0
    px = px0
    py = py0
    err = 1e-15
    status = 0 # Hit nothing
    
    # Time reset
    t = 0
    for i in range(n):

        # Store position
        xlist[i] = x
        ylist[i] = y
        pxlist[i] = px
        pylist[i] = py
        errlist[i] = err
        hlist[i] = h

        # Integrate time period
        dt = duration*(i+1)/n
        while t < dt:

            # Adaptive symplectic euler/midpoint
            x1,y1,px1,py1=symplectic_euler_step(h,x,y,px,py)
            x2,y2,px2,py2=symplectic_verlet_step(h,x,y,px,py)

            # Relative local error of step
            err = math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1)/(x2*x2+y2*y2))

            # Accept the step only if the weighted error is no more than the
            # tolerance tol.  Estimate an h that will yield an error of tol on
            # the next step and use 0.8 of this value to avoid failures.
            if err < tol and h > hmin:
                # Accept step
                x = x2
                y = y2
                px = px2
                py = py2

                # Forward time by step
                t = t+h
                h = max(hmin, h*max(0.1, 0.8*math.sqrt(tol/err)))
            else:
                # No accept, reduce h to half
                h = max(hmin, 0.5*h)

            # Check if we hit something
            if status == 0:
                rx = x-moon_pos_x
                ry = y
                r = math.sqrt(rx*rx+ry*ry)
                r_low = (lunar_orbit-orbit_range)/unit_len
                r_high = (lunar_orbit+orbit_range)/unit_len
                if r > r_low and r < r_high:
                    status = 1 # Hit moon orbit

                    # Project impulse onto radius vector
                    pr = (px*rx+py*ry)/r;

                    # Change impulse to capture orbit
                    px = px-pr*rx/r
                    py = py-pr*ry/r
                    p = math.sqrt(px*px+py*py)

                    px = (moon_orbit_vel/unit_vel)*px/p
                    py = (moon_orbit_vel/unit_vel)*py/p

                    #return status

            if status == 1:
                r = (x-earth_pos_x)*(x-earth_pos_x)+y*y
                r_high = earth_radius/unit_len
                if r < r_high*r_high:
                    status = -1 # Hit earth surface
                    return status

    return status
