from .constants import *
from .derivations import *
from .planets import *


def euler_step(h, x, y, p_x, p_y):
    """takes a single time step of the symplectic euler algorithm"""
    v_x = p_x + y
    x = (x + h*(v_x+p_y*h)) / (1.0 + h**2)
    v_y = p_y - x
    y += v_y*h

    Pdot_x, Pdot_y = Pdot(x, y, p_x, p_y)
    p_x += Pdot_x*h
    p_y += Pdot_y*h
    return x, y, p_x, p_y


def verlet_step(h, x, y, p_x, p_y):
    """takes a half step, then another half step in the symplectic Verlet algorithm"""
    half_h = h/2
    denominator = 1.0/(1+half_h**2)

    v_x = p_x-x
    x = (x + half_h*(v_x+p_y*half_h)) * denominator
    v_y = p_y - x
    y += v_y*half_h

    Pdot_x, Pdot_y = Pdot(x, y, p_x, p_y)
    p_x = (p_x+(2.0*Pdot_x+(Pdot_y*2 + p_x)*half_h)*half_h) * denominator
    p_y += (Pdot_y*2)*half_h

    v_x = p_x + y
    v_y = p_y - x
    x += v_x*half_h
    y += v_y*half_h
    return x, y, p_x, p_y


def relative_error(vec1, vec2):
    x1, y1 = vec1
    x2, y2 = vec2
    return sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1)/(x2*x2+y2*y2))


def symplectic(x0, y0, p0_x, p0_y, max_iter=1000, target=target(celestials.MOON)):
    h = h_default
    x, y, p_x, p_y = [x0, y0, p0_x, p0_y]

    for i in range(max_iter):

        x_euler, y_euler, p_euler_x, p_euler_y = euler_step(
            h, x0, y0, p0_x, p0_y)
        x_verlet, y_verlet, p_verlet_x, p_verlet_y = verlet_step(
            h, x0, y0, p0_x, p0_y)
        err = relative_error([x_euler, y_euler], [x_verlet, y_verlet])
        if err < tol or h <= hmin:
            x = x_verlet
            y = y_verlet
            p_x = p_verlet_x
            p_y = p_verlet_y

            t += h
            h = max(hmin, h*max(0.1, 0.8*sqrt(tol/err)))
            # TODO: explain this with /HH's new comments. 0.8 is chosen empirically
            # old explanation below:
            """Accept the step only if the weighted error is no more than the
            tolerance tol.  Estimate an h that will yield an error of tol on
            the next step and use 0.8 of this value to avoid failures."""

        else:
            h = max(hmin, h/2)

        """Are we nearly there yet? (calculate distance)"""
        target_distance_x = x - target.position_x
        target_distance_y = y - target.position_y
        target_distance = sqrt(target_distance_x**2 + target_distance_y**2)
        smallest_distance = min(smallest_distance, target_distance)

        """For real though, are we there yet? (did we actually hit?)"""
        orbital_radius_lower_bound, orbital_radius_upper_bound = target.get_orbital_bounds()

    return result
