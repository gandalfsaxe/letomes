from .constants import *
import json

# Write constants to text file
constants_dict = {
    "EARTH_ALTITUDE": EARTH_ALTITUDE,
    "LUNAR_ALTITUDE": LUNAR_ALTITUDE,
    "ORBITAL_TOLERANCE": ORBITAL_TOLERANCE,
    "h_default": h_default,
    "h_min": h_min,
    "tol": tol,
    "earth_moon_distance": earth_moon_distance,
    "lunar_orbit_duration": lunar_orbit_duration,
    "earth_radius": earth_radius,
    "earth_mass": earth_mass,
    "lunar_radius": lunar_radius,
    "lunar_mass": lunar_mass,
    "G": G,
    "day": day,
    "k": k,
    "lunar_position_x": lunar_position_x,
    "earth_position_x": earth_position_x,
    "L1_position_x": L1_position_x,
    "leo_radius": leo_radius,
    "llo_radius": llo_radius,
    "leo_velocity": leo_velocity,
    "llo_velocity": llo_velocity,
    "unit_length": unit_length,
    "unit_time": unit_time,
    "unit_velocity": unit_velocity,
    "leo_radius_nondim": leo_radius_nondim,
    "leo_velocity_nondim": leo_velocity_nondim,
}

with open("constants.json", "w") as file:
    file.write(json.dumps(constants_dict, indent=2))
