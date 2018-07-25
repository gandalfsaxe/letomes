from enum import Enum

from .constants import *


class planet:
    def __init__(self, celestial):
        self.celestial = celestial
        if celestial == celestials.MOON:
            self.orbital_radius = llo_radius
            self.orbital_velocity = llo_velocity
            self.position_x = lunar_position_x
            self.position_y = 0
            self.celestial_radius = lunar_radius
            self.celestial_mass = lunar_mass
            self.altitude = LUNAR_ALTITUDE
            self.orbital_radius_nondim = None
            self.orbital_velocity_nondim = None
        elif celestial == celestials.EARTH:
            self.orbital_radius = leo_radius
            self.orbital_velocity = leo_velocity
            self.position_x = earth_position_x
            self.position_y = 0
            self.celestial_radius = earth_radius
            self.celestial_mass = earth_mass
            self.altitude = EARTH_ALTITUDE
            self.orbital_radius_nondim = leo_radius_nondim
            self.orbital_velocity_nondim = leo_velocity_nondim
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

    def get_orbital_bounds(self):
        """returns [lower_bound, upper_bound] for successful celestial orbit"""
        upper_bound = (self.orbital_radius + ORBITAL_TOLERANCE) / unit_length
        lower_bound = (self.orbital_radius - ORBITAL_TOLERANCE) / unit_length
        return [lower_bound, upper_bound]


class celestials(Enum):
    EARTH = 0
    MOON = 1
    MARS = 2
