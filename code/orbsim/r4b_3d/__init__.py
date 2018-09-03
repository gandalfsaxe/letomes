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
    EARTH_MOON_DISTANCE,
    EARTH_RADIUS,
    LUNAR_MASS,
    LUNAR_ORBITAL_DURATION,
    LUNAR_RADIUS,
)

### SIMULATION CONSTANTS ###
# class: Planets (planets.py)
EARTH_ALTITUDE = 160.0  # km
LUNAR_ALTITUDE = 100.0  # km
ORBITAL_TOLERANCE = 10  # km

# function: symplectic (integrators.py)
h_DEFAULT = 1e-6  # dimless time
h_MIN_DEFAULT = 1e-10  # dimless time
STEP_ERROR_TOLERANCE = 1e-9  # dimless time


# Dimensionless constants
k = LUNAR_MASS / (EARTH_MASS + LUNAR_MASS)  # dimless

# Note that Y for both Earth and Moon is always zero in (X,Y) system
LUNAR_POSITION_X = 1 - k
EARTH_POSITION_X = -k
L1_POSITION_X = 1 - pow(k / 3, 1 / 3)


### DERIVED BOUNDARY CONDITIONS ###
LEO_RADIUS = EARTH_RADIUS + EARTH_ALTITUDE  # km
LLO_RADIUS = LUNAR_RADIUS + LUNAR_ALTITUDE  # km

LEO_VELOCITY = sqrt(G * EARTH_MASS / (LEO_RADIUS * 1000.0)) / 1000.0  # km/s
LLO_VELOCITY = sqrt(G * LUNAR_MASS / (LLO_RADIUS * 1000.0)) / 1000.0  # km/s


### NONDIMENSIONALIZATION ###
# Characteristic units
UNIT_LENGTH = EARTH_MOON_DISTANCE  # km
UNIT_TIME = LUNAR_ORBITAL_DURATION / (2.0 * pi)  # days
UNIT_VELOCITY = UNIT_LENGTH / (UNIT_TIME * DAY)  # km/s

# Nondimensionalized boundary conditions
LEO_RADIUS_NONDIM = LEO_RADIUS / UNIT_LENGTH  # dimless
LEO_VELOCITY_NONDIM = LEO_VELOCITY / UNIT_VELOCITY  # dimless


def update_constants_json():
    """ Write constant to constants.json file in same directory"""

    # Write constants to text file
    constants_dict = {
        ### SIMULATION CONSTANTS ###
        "EARTH_ALTITUDE": EARTH_ALTITUDE,
        "LUNAR_ALTITUDE": LUNAR_ALTITUDE,
        "ORBITAL_TOLERANCE": ORBITAL_TOLERANCE,
        "h_DEFAULT": h_DEFAULT,
        "h_MIN": h_MIN_DEFAULT,
        "STEP_ERROR_TOLERANCE": STEP_ERROR_TOLERANCE,
        # Dimensionless constants
        "k": k,
        "LUNAR_POSITION_X": LUNAR_POSITION_X,
        "EARTH_POSITION_X": EARTH_POSITION_X,
        "L1_POSITION_X": L1_POSITION_X,
        ### DERIVED BOUNDARY CONDITIONS ###
        "LEO_RADIUS": LEO_RADIUS,
        "LLO_RADIUS": LLO_RADIUS,
        "LEO_VELOCITY": LEO_VELOCITY,
        "LLO_VELOCITY": LLO_VELOCITY,
        ### NONDIMENSIONALIZATION ###
        # Characteristic units
        "UNIT_LENGTH": UNIT_LENGTH,
        "UNIT_TIME": UNIT_TIME,
        "UNIT_VELOCITY": UNIT_VELOCITY,
        # Nondimensionalized boundary conditions
        "LEO_RADIUS_NONDIM": LEO_RADIUS_NONDIM,
        "LEO_VELOCITY_NONDIM": LEO_VELOCITY_NONDIM,
    }

    orbsim_path = os.path.dirname(os.path.abspath(__file__))

    with open(orbsim_path + "/constants.json", "w", newline="\n") as file:
        file.write(json.dumps(constants_dict, indent=2))


if __name__ == "__main__":
    update_constants_json()
