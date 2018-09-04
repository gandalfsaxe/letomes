"""
Constants common to all simulations.

Unless otherwise noted, all units will be in:
- Mass:   kg
- Length: km
- Time:   days  TODO: Change to seconds due to better fit with typical time step size
"""
import json
import os

############### TABLE / PHYSICAL CONSTANTS ###############
# See physical_constants_and_units.nb, but can be looked up in any table / Wikipedia

# Physical constants
G = 6.67384e-11 / 1000 ** 3  # kg^-1 km^3 s^-2
DAY = 24.0 * 3600.0  # s

# Solar system quantities
a_EARTH = 1.49597887e8  # km (semi major axis of Earth's orbit)
T_EARTH = 3.1558149e7  # s (orbital period of Earth)

# Sun constants
SUN_MASS = 1.988435e30  # kg

# Earth constants
EARTH_RADIUS = 6367.4447  # km
EARTH_MASS = 5.9721986e24  # kg

# Lunar quantities
LUNAR_RADIUS = 1737.1  # km
LUNAR_MASS = 7.34767309e22  # kg
EARTH_MOON_DISTANCE = 384400.0  # km
LUNAR_ORBITAL_DURATION = 27.322  # days

# Mars quantities
MARS_RADIUS = 3389.5  # km
MARS_MASS = 6.41693e23  # kg


############### DERIVED CONSTANTS ###############
MU_SUN = G * SUN_MASS  # km^-3 s^2
MU_EARTH = G * EARTH_MASS  # km^-3 s^2
MU_MARS = G * MARS_MASS  # km^-3 s^2


def update_constants_json():
    """ Write constants to constants.json file in same directory"""

    # Write constants to text file
    constants_dict = {
        ############### TABLE / PHYSICAL CONSTANTS ###############
        "G": G,
        "DAY": DAY,
        "a_EARTH": a_EARTH,
        "T_EARTH": T_EARTH,
        "SUN_MASS": SUN_MASS,
        "EARTH_RADIUS": EARTH_RADIUS,
        "EARTH_MASS": EARTH_MASS,
        "LUNAR_RADIUS": LUNAR_RADIUS,
        "LUNAR_MASS": LUNAR_MASS,
        "EARTH_MOON_DISTANCE": EARTH_MOON_DISTANCE,
        "LUNAR_ORBIT_DURATION": LUNAR_ORBITAL_DURATION,
        "MARS_RADIUS": MARS_RADIUS,
        "MARS_MASS": MARS_MASS,
        ############### DERIVED CONSTANTS ###############
        "MU_SUN": MU_SUN,
        "MU_EARTH": MU_EARTH,
        "MU_MARS": MU_MARS,
    }

    orbsim_path = os.path.dirname(os.path.abspath(__file__))

    with open(orbsim_path + "/constants.json", "w", newline="\n") as file:
        file.write(json.dumps(constants_dict, indent=2))


if __name__ == "__main__":
    update_constants_json()
