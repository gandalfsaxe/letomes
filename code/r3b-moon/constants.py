from math import pi,sqrt,pow
"""
Unless otherwise noted, all units will be in:
Mass:   kg
Length: km
Time:   days
"""

### USER DEFINED CONSTANTS ###
EARTH_ALTITUDE = 160.0  # km
LUNAR_ALTITUDE = 100.0  # km


### TABLE / PHYSICAL CONSTANTS ###
earth_moon_distance = 384400.0  # km
lunar_orbit_duration = 27.322  # days

earth_radius = 6367.4447  # km
earth_mass = 5.9721986e24  # kg

lunar_radius = 1737.1  # km
lunar_mass = 7.34767309e22  # kg

G = 6.67384e-11  # m^3 kg^-1 s^-2
day = 24.0*3600.0  # s

# Dimensionless constants
k = lunar_mass / (earth_mass + lunar_mass)  # 1


### DERIVED BOUNDARY CONDITIONS ###
leo_radius = earth_radius + EARTH_ALTITUDE  # km
llo_radius = lunar_radius + LUNAR_ALTITUDE  # km

leo_velocity = sqrt(G*earth_mass / (leo_radius*1000.0))/1000.0  # km/s
llo_velocity = sqrt(G*lunar_mass / (llo_radius*1000.0))/1000.0  # km/s


### NONDIMENSIONALIZATION ###
# Characteristic units
unit_length = earth_moon_distance  # km
unit_time = lunar_orbit_duration/(2.0*pi)  # days
unit_velocity = unit_length / (unit_time*day) # km/s

### Nondimensionalized boundary conditions
leo_radius_nondim = leo_radius / unit_length
leo_radius_velocity_nondim = leo_velocity / unit_velocity
