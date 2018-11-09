"""
Constants specific to R4B-3D (Restricted 4-Body Problem in 3 Dimensions)

Unless otherwise noted, all units will be in:
- Mass:   kg
- Length: km
- Time:   days  TODO: Change to seconds due to better fit with typical time step size

Variable name conventions:
- non_dim: dimensionless (nondimensionalized)
"""
import json
import os
from math import pi, sqrt

from orbsim import (
    G,
    DAY,
    EARTH_MASS,
    EARTH_RADIUS,
    LUNAR_MASS,
    LUNAR_RADIUS,
    a_EARTH,
    T_EARTH,
    SUN_MU,
    EARTH_MU,
    MARS_MU,
)

############### SIMULATION CONSTANTS ###############

# class: Planets (planets.py)
EARTH_ALTITUDE = 160.0  # km
LUNAR_ALTITUDE = 100.0  # km
ORBITAL_TOLERANCE = 10  # km

# function: symplectic (integrators.py)
DAY0 = 0  # start day of simulation, day=0 is 2019-01-01 00:00:00
h_DEFAULT = 1e-6  # dimless time
h_MIN_DEFAULT = 1e-10  # dimless time
STEP_ERROR_TOLERANCE = 1e-9  # dimless time


############### CHARACTERISTIC UNITS ###############

UNIT_LENGTH = a_EARTH  # km/AU
# (This is the precise definition, see https://en.wikipedia.org/wiki/Astronomical_unit)
UNIT_TIME = T_EARTH  # 1 year in s/year
UNIT_VELOCITY = 4.7403885  # km/s (or 1 AU/y in km/s)
UNIT_VELOCITY2 = UNIT_LENGTH / (UNIT_TIME * DAY)  # km/s (just a check)


############### DERIVED BOUNDARY CONDITIONS ###############

# Initial orbit (Earth)
LEO_RADIUS = EARTH_RADIUS + EARTH_ALTITUDE  # km
LEO_VELOCITY = sqrt(G * EARTH_MASS / (LEO_RADIUS))  # km/s

# Target orbit (Moon)
LLO_RADIUS = LUNAR_RADIUS + LUNAR_ALTITUDE  # km
LLO_VELOCITY = sqrt(G * LUNAR_MASS / (LLO_RADIUS))  # km/s

# Stationary Sun
SUN_R = 0
get_circular_orbit_period = pi / 4
SUN_PHI = 0

############### NONDIMENSIONALIZATION ###############

# Nondimensionalized boundary conditions
LEO_RADIUS_NONDIM = LEO_RADIUS / UNIT_LENGTH  # dimless
LEO_VELOCITY_NONDIM = LEO_VELOCITY / UNIT_VELOCITY  # dimless

# Nondimensionalized standard gravitational parameters
SUN_ETA = UNIT_TIME ** 2 / UNIT_LENGTH ** 3 * SUN_MU
EARTH_ETA = UNIT_TIME ** 2 / UNIT_LENGTH ** 3 * EARTH_MU
MARS_ETA = UNIT_TIME ** 2 / UNIT_LENGTH ** 3 * MARS_MU


def update_constants_json():
    """ Write constant to constants.json file in same directory"""

    # Write constants to text file
    constants_dict = {
        ############### SIMULATION CONSTANTS ###############
        "EARTH_ALTITUDE": EARTH_ALTITUDE,
        "LUNAR_ALTITUDE": LUNAR_ALTITUDE,
        "ORBITAL_TOLERANCE": ORBITAL_TOLERANCE,
        "h_DEFAULT": h_DEFAULT,
        "h_MIN": h_MIN_DEFAULT,
        "STEP_ERROR_TOLERANCE": STEP_ERROR_TOLERANCE,
        ############### CHARACTERISTIC UNITS ###############
        "UNIT_LENGTH": UNIT_LENGTH,
        "UNIT_TIME": UNIT_TIME,
        "UNIT_VELOCITY": UNIT_VELOCITY,
        "UNIT_VELOCITY2": UNIT_VELOCITY2,
        ############### DERIVED BOUNDARY CONDITIONS ##################
        "LEO_RADIUS": LEO_RADIUS,
        "LEO_VELOCITY": LEO_VELOCITY,
        "LLO_RADIUS": LLO_RADIUS,
        "LLO_VELOCITY": LLO_VELOCITY,
        "SUN_R": SUN_R,
        "get_circular_orbit_period": get_circular_orbit_period,
        "SUN_PHI": SUN_PHI,
        ############### NONDIMENSIONALIZATION ###############
        "LEO_RADIUS_NONDIM": LEO_RADIUS_NONDIM,
        "LEO_VELOCITY_NONDIM": LEO_VELOCITY_NONDIM,
        "SUN_ETA": SUN_ETA,
        "EARTH_ETA": EARTH_ETA,
        "MARS_ETA": MARS_ETA,
    }

    orbsim_path = os.path.dirname(os.path.abspath(__file__))

    with open(orbsim_path + "/constants.json", "w", newline="\n") as file:
        file.write(json.dumps(constants_dict, indent=2))


if __name__ == "__main__":
    update_constants_json()
