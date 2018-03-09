"""
Reduced 3-Body Problem Solver Module
====================================
A collection of various numerical solvers for the reduced 3-body problem consisting of two larger masses (Earth, Moon) and one smaller moving in their gravitaional field (a satellite). The solution assumes Earth-Moon center of mass as origin and a cartesian x-y coordinate system rotating with the lines connecting the Earth and Moon (non-interial frame accounted for in the equations of motion).

Functions:
    euler: Solves by Euler method explicitely, implicitely or symplectically.

We assume **TODO FILL OUT HERE!

"""

from math import pi,sqrt
import numpy as np
from numbapro import *
from const import *

@jit
def F(x,y):
    mux = mu+x
    mux2 = mux*mux
    mumx = 1-mux
    mumx2 = mumx*mumx
    y2 = y*y
    denum1 = 1.0/((mux2+y2)*sqrt(mux2+y2))
    denum2 = 1.0/((mumx2+y2)*sqrt(mumx2+y2))
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

@jit #('void(int64, float64, float64, float64, float64, float64, float64, float64[:], float64[:], float64[:], float64[:])')
def symplectic(n,duration,x0,y0,px0,py0,xlist,ylist,pxlist,pylist,errlist,hlist,info):

    # Initialize initial conditions
    h = 1e-6
    hmin = 1e-10
    tol = 1e-9
    maxsteps = duration
    x = x0
    y = y0
    px = px0
    py = py0
    err = 1e-15
    status = 1
    target_dist = 1
    target = 1; target_pos_x = moon_pos_x
    #target = 2; target_pos_x = L1_pos_x
    target_pos_y = 0
    
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
        count = 0
        while t < dt:
            # Safety on iterations
            count += 1
            if count > 10000000:
                count = 0
                hmin = 2*hmin
            
            # Adaptive symplectic euler/midpoint
            x1,y1,px1,py1 = symplectic_euler_step(h,x,y,px,py)
            x2,y2,px2,py2 = symplectic_verlet_step(h,x,y,px,py)

            # Relative local error of step
            err = sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1)/(x2*x2+y2*y2))

            # Accept the step only if the weighted error is no more than the
            # tolerance tol.  Estimate an h that will yield an error of tol on
            # the next step and use 0.8 of this value to avoid failures.
            if err < tol or h <= hmin:

                # Accept step
                x = x2
                y = y2
                px = px2
                py = py2

                # Forward time by step
                t = t+h
                h = max(hmin, h*max(0.1, 0.8*sqrt(tol/err)))

            else:
                # No accept, reduce h to half
                h = max(hmin, 0.5*h)

            # How close are we to the moon?
            rx = x-target_pos_x
            ry = y-target_pos_y
            r = sqrt(rx*rx+ry*ry)
            target_dist = min(target_dist,r)

            # Check if we hit the target
            if status == 1:
                if target == 1:
                    r_low = (lunar_orbit-orbit_range)/unit_len
                    r_high = (lunar_orbit+orbit_range)/unit_len
                else:
                    r_low = 0
                    r_high = orbit_range/unit_len

                if r > r_low and r < r_high:

                    # Current velocity
                    vx = px+y
                    vy = py-x

                    if target == 1:

                        # Project velocity onto radius vector and subtract
                        # so velocity vector is along orbit
                        vr = (vx*rx+vy*ry)/r
                        vx = vx-vr*rx/r
                        vy = vy-vr*ry/r
                    
                        # Now ajust velocity to lunar orbit velocity
                        vt = sqrt(vx*vx+vy*vy)
                        px = (lunar_orbit_vel/unit_vel)*vx/vt-y
                        py = (lunar_orbit_vel/unit_vel)*vy/vt+x

                        # Total velocity change
                        dv = sqrt(vr*vr+(vt-lunar_orbit_vel/unit_vel)*(vt-lunar_orbit_vel/unit_vel))
                    else:
                        dv = sqrt(vx*vx+vy*vy)
                    
                    # Store info
                    info[0] = dv
                    info[1] = t

                    # Finish?
                    status = -10000+dv
                    if n == 1:
                        return status

            # Check if we hit the earth
            r = (x-earth_pos_x)*(x-earth_pos_x)+y*y
            r_high = earth_radius/unit_len
            if r < r_high*r_high:
                return 100 # Hit earth surface

    if status >= 0:
        status = target_dist

    return status
