import json
import os
from math import pi, pow, sqrt

from orbsim import (
    G,
    day,
    earth_mass,
    earth_moon_distance,
    earth_radius,
    lunar_mass,
    lunar_orbit_duration,
    lunar_radius,
)

"""
Unless otherwise noted, all units will be in:
- Mass:   kg
- Length: km
- Time:   days

Variable name conventions:
- non_dim: dimensionless (nondimensionalized)
"""

### SIMULATION CONSTANTS ###
EARTH_ALTITUDE = 160.0  # km
LUNAR_ALTITUDE = 100.0  # km

ORBITAL_TOLERANCE = 10  # km
h_default = 1e-6  # dimless time
h_min = 1e-10  # dimless time
tol = 1e-9  # dimless time


# Dimensionless constants
k = lunar_mass / (earth_mass + lunar_mass)  # dimless

# Note that Y for both Earth and Moon is always zero in (X,Y) system
lunar_position_x = 1 - k
earth_position_x = -k
L1_position_x = 1 - pow(k / 3, 1 / 3)


### DERIVED BOUNDARY CONDITIONS ###
leo_radius = earth_radius + EARTH_ALTITUDE  # km
llo_radius = lunar_radius + LUNAR_ALTITUDE  # km

leo_velocity = sqrt(G * earth_mass / (leo_radius * 1000.0)) / 1000.0  # km/s
llo_velocity = sqrt(G * lunar_mass / (llo_radius * 1000.0)) / 1000.0  # km/s


### NONDIMENSIONALIZATION ###
# Characteristic units
unit_length = earth_moon_distance  # km
unit_time = lunar_orbit_duration / (2.0 * pi)  # days
unit_velocity = unit_length / (unit_time * day)  # km/s

# Nondimensionalized boundary conditions
leo_radius_nondim = leo_radius / unit_length  # dimless
leo_velocity_nondim = leo_velocity / unit_velocity  # dimless


def update_constants_json():

    # Write constants to text file
    constants_dict = {
        ### SIMULATION CONSTANTS ###
        "EARTH_ALTITUDE": EARTH_ALTITUDE,
        "LUNAR_ALTITUDE": LUNAR_ALTITUDE,
        "ORBITAL_TOLERANCE": ORBITAL_TOLERANCE,
        "h_default": h_default,
        "h_min": h_min,
        "tol": tol,
        # Dimensionless constants
        "k": k,
        "lunar_position_x": lunar_position_x,
        "earth_position_x": earth_position_x,
        "L1_position_x": L1_position_x,
        ### DERIVED BOUNDARY CONDITIONS ###
        "leo_radius": leo_radius,
        "llo_radius": llo_radius,
        "leo_velocity": leo_velocity,
        "llo_velocity": llo_velocity,
        ### NONDIMENSIONALIZATION ###
        # Characteristic units
        "unit_length": unit_length,
        "unit_time": unit_time,
        "unit_velocity": unit_velocity,
        # Nondimensionalized boundary conditions
        "leo_radius_nondim": leo_radius_nondim,
        "leo_velocity_nondim": leo_velocity_nondim,
    }

    orbsim_path = os.path.dirname(os.path.abspath(__file__))

    with open(orbsim_path + "/constants.json", "w", newline="\n") as file:
        file.write(json.dumps(constants_dict, indent=2))


if __name__ == "__main__":
    update_constants_json()
