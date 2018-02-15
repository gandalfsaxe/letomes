from math import pi,sqrt,pow

# Table constants
earth_moon_distance = 384400.0 # km
moon_orbit_duration = 27.322 # days
earth_radius = 6367.4447 # km
earth_mass = 5.9721986e24
moon_mass = 7.34767309e22
G = 6.67384e-11 # m^3 kg^-1 s^-2
moon_radius = 1737.1 # km
leo_orbit = 160.0+earth_radius # km
lunar_orbit = 100.0+moon_radius # km
orbit_range = 10.0 # km
day = 24.0*3600.0 # s

# Units
unit_len = earth_moon_distance # km
unit_time = moon_orbit_duration/(2.0*pi) # days
unit_vel = unit_len/(unit_time*day) # km/s

# Gravitational constants
mu = moon_mass/(earth_mass+moon_mass) # 1

# Calculation constants
leo_orbit_vel = sqrt(G*earth_mass/(leo_orbit*1000.0))/1000.0 # km/s
lunar_orbit_vel = sqrt(G*moon_mass/(lunar_orbit*1000.0))/1000.0 # km/s
moon_pos_x = 1-mu
earth_pos_x = -mu
L1_pos_x = (1-pow(mu/3.0,1.0/3.0))
