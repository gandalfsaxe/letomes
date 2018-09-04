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
    MU_SUN,
    MU_EARTH,
    MU_MARS,
)

############### SIMULATION CONSTANTS ###############

# class: Planets (planets.py)
EARTH_ALTITUDE = 160.0  # km
LUNAR_ALTITUDE = 100.0  # km
ORBITAL_TOLERANCE = 10  # km

# function: symplectic (integrators.py)
h_DEFAULT = 1e-6  # dimless time
h_MIN_DEFAULT = 1e-10  # dimless time
STEP_ERROR_TOLERANCE = 1e-9  # dimless time


############### CHARACTERISTIC UNITS ###############

UNIT_LENGTH = a_EARTH  # km
UNIT_TIME = T_EARTH  # days
UNIT_VELOCITY = 4.7403885  # km/s
UNIT_VELOCITY2 = UNIT_LENGTH / (UNIT_TIME * DAY)  # km/s (just a check)


############### DERIVED BOUNDARY CONDITIONS ###############

# Initial orbit (Earth)
LEO_RADIUS = EARTH_RADIUS + EARTH_ALTITUDE  # km
LEO_VELOCITY = sqrt(G * EARTH_MASS / (LEO_RADIUS * 1000.0)) / 1000.0  # km/s

# Target orbit (Moon)
LLO_RADIUS = LUNAR_RADIUS + LUNAR_ALTITUDE  # km
LLO_VELOCITY = sqrt(G * LUNAR_MASS / (LLO_RADIUS * 1000.0)) / 1000.0  # km/s

# Stationary Sun
R_SUN = 0
THETA_SUN = 0
PHI_SUN = 0

############### NONDIMENSIONALIZATION ###############

# Nondimensionalized boundary conditions
LEO_RADIUS_NONDIM = LEO_RADIUS / UNIT_LENGTH  # dimless
LEO_VELOCITY_NONDIM = LEO_VELOCITY / UNIT_VELOCITY  # dimless

# Nondimensionalized standard gravitational parameters
ETA_SUN = UNIT_TIME ** 2 / UNIT_LENGTH ** 3 * MU_SUN
ETA_EARTH = UNIT_TIME ** 2 / UNIT_LENGTH ** 3 * MU_EARTH
ETA_MARS = UNIT_TIME ** 2 / UNIT_LENGTH ** 3 * MU_MARS


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
        "R_SUN": R_SUN,
        "THETA_SUN": THETA_SUN,
        "PHI_SUN": PHI_SUN,
        ############### NONDIMENSIONALIZATION ###############
        "LEO_RADIUS_NONDIM": LEO_RADIUS_NONDIM,
        "LEO_VELOCITY_NONDIM": LEO_VELOCITY_NONDIM,
        "ETA_SUN": ETA_SUN,
        "ETA_EARTH": ETA_EARTH,
        "ETA_MARS": ETA_MARS,
    }

    orbsim_path = os.path.dirname(os.path.abspath(__file__))

    with open(orbsim_path + "/constants.json", "w", newline="\n") as file:
        file.write(json.dumps(constants_dict, indent=2))


if __name__ == "__main__":
    update_constants_json()
