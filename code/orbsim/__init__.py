import json
import os

"""
Unless otherwise noted, all units will be in:
- Mass:   kg
- Length: km
- Time:   days
"""

### TABLE / PHYSICAL CONSTANTS ###
earth_radius = 6367.4447  # km
earth_mass = 5.9721986e24  # kg

lunar_radius = 1737.1  # km
lunar_mass = 7.34767309e22  # kg

earth_moon_distance = 384400.0  # km
lunar_orbit_duration = 27.322  # days

G = 6.67384e-11  # m^3 kg^-1 s^-2
day = 24.0 * 3600.0  # s


def update_constants_json():

    # Write constants to text file
    constants_dict = {
        "earth_radius": earth_radius,
        "earth_mass": earth_mass,
        "lunar_radius": lunar_radius,
        "lunar_mass": lunar_mass,
        "earth_moon_distance": earth_moon_distance,
        "lunar_orbit_duration": lunar_orbit_duration,
        "G": G,
        "day": day,
    }

    orbsim_path = os.path.dirname(os.path.abspath(__file__))

    with open(orbsim_path + "/constants.json", "w", newline="\n") as file:
        file.write(json.dumps(constants_dict, indent=2))


if __name__ == "__main__":
    update_constants_json()
