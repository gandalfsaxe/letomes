from math import pi,sqrt,pow

# Table constants
earth_moon_distance = 384400.0 # km
moon_orbit_duration = 27.322 # days
earth_radius = 6367.4447 # km
earth_mass = 5.9721986e24
moon_mass = 7.34767309e22
G = 6.67384e-11 # m^3 kg^-1 s^-2
lunar_radius = 1737.1 # km
leo_radius = 160.0+earth_radius # km
llo_radius = 100.0+lunar_radius # km
ORBITAL_TOLERANCE = 10.0 # km
day = 24.0*3600.0 # s

# Units
unit_length = earth_moon_distance # km
unit_time = moon_orbit_duration/(2.0*pi) # days
unit_velocity = unit_length/(unit_time*day) # km/s

# Gravitational constants
k = moon_mass/(earth_mass+moon_mass) # 1

# Calculation constants
leo_velocity = sqrt(G*earth_mass/(leo_radius*1000.0))/1000.0 # km/s
llo_velocity = sqrt(G*moon_mass/(llo_radius*1000.0))/1000.0 # km/s
lunar_position_x = 1-k
earth_position_x = -k
L1_position_x = (1-pow(k/3.0,1.0/3.0))
