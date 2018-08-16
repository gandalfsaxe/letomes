from enum import Enum

from numba import jit

from . import EARTH_MASS, EARTH_RADIUS, LUNAR_MASS, LUNAR_RADIUS
from .r3b_2d import (
    EARTH_ALTITUDE,
    LUNAR_ALTITUDE,
    ORBITAL_TOLERANCE,
    EARTH_POSITION_X,
    LEO_RADIUS,
    LEO_RADIUS_NONDIM,
    LEO_VELOCITY,
    LEO_VELOCITY_NONDIM,
    LLO_RADIUS,
    LLO_VELOCITY,
    LUNAR_POSITION_X,
    UNIT_LENGTH,
    UNIT_VELOCITY,
)


class Planet:
    def __init__(self, celestial):
        self.celestial = celestial
        if celestial == celestials.MOON:
            self.orbital_radius = LLO_RADIUS
            self.orbital_velocity = LLO_VELOCITY
            self.position_x = LUNAR_POSITION_X
            self.position_y = 0
            self.celestial_radius = LUNAR_RADIUS
            self.celestial_mass = LUNAR_MASS
            self.altitude = LUNAR_ALTITUDE
            self.orbital_radius_nondim = self.orbital_radius / UNIT_LENGTH
            self.orbital_velocity_nondim = self.orbital_velocity / UNIT_VELOCITY
        elif celestial == celestials.EARTH:
            self.orbital_radius = LEO_RADIUS
            self.orbital_velocity = LEO_VELOCITY
            self.position_x = EARTH_POSITION_X
            self.position_y = 0
            self.celestial_radius = EARTH_RADIUS
            self.celestial_mass = EARTH_MASS
            self.altitude = EARTH_ALTITUDE
            self.orbital_radius_nondim = LEO_RADIUS_NONDIM
            self.orbital_velocity_nondim = LEO_VELOCITY_NONDIM
        elif celestial == celestials.MARS:
            self.orbital_radius = None
            self.orbital_velocity = None
            self.position_x = None
            self.position_y = None
            self.celestial_radius = None
            self.celestial_mass = None
            self.altitude = None
            self.orbital_radius_nondim = None
            self.orbital_velocity_nondim = None


@jit
def get_orbital_bounds(celestial):
    """returns [lower_bound, upper_bound] for successful celestial orbit"""
    planet = Planet(celestial)
    lower_bound = (planet.orbital_radius - ORBITAL_TOLERANCE) / UNIT_LENGTH
    upper_bound = (planet.orbital_radius + ORBITAL_TOLERANCE) / UNIT_LENGTH
    return [lower_bound, upper_bound]


@jit
def get_critical_bounds(celestial):
    planet = Planet(celestial)
    return (planet.celestial_radius / UNIT_LENGTH) ** 2


class celestials(Enum):
    EARTH = 0
    MOON = 1
    MARS = 2
