#pragma once

#define G 6.67384e-20
#define DAY 86400.0
#define a_EARTH 149597887.0
#define T_EARTH 31558149.0
#define SUN_MASS 1.988435e+30
#define EARTH_RADIUS 6367.4447
#define EARTH_MASS 5.9721986e+24
#define LUNAR_RADIUS 1737.1
#define LUNAR_MASS 7.34767309e+22
#define EARTH_MOON_DISTANCE 384400.0
#define LUNAR_ORBIT_DURATION 27.322
#define MARS_RADIUS 3389.5
#define MARS_MASS 6.41693e+23
#define SUN_MU 132704970404.0
#define EARTH_MU 398574.97904624
#define MARS_MU 42825.5641112

#define EARTH_ALTITUDE 160.0
#define LUNAR_ALTITUDE 100.0
#define ORBITAL_TOLERANCE 10
#define h_DEFAULT 1e-06
#define h_MIN 1e-10
#define STEP_ERROR_TOLERANCE 1e-09
#define K 0.012153601852294929
#define LUNAR_POSITION_X 0.987846398147705
#define EARTH_POSITION_X -0.012153601852294929
#define L1_POSITION_X 0.8405854649886768
#define LEO_RADIUS 6527.4447
#define LLO_RADIUS 1837.1
#define LEO_VELOCITY 7.8141800786375315
#define LLO_VELOCITY 1.6337906619944857
#define UNIT_LENGTH 384400.0
#define UNIT_TIME 4.348431355156764
#define UNIT_VELOCITY 1.0231446033517257
#define LEO_RADIUS_NONDIM 0.016980865504682623
#define LEO_VELOCITY_NONDIM 7.6374151347121515

//#define LEO_VELOCITY sqrt(G * EARTH_MASS / (LEO_RADIUS))
//#define LLO_VELOCITY sqrt(G * LUNAR_MASS / (LLO_RADIUS))
//#define LEO_RADIUS_NONDIM LEO_RADIUS / UNIT_LENGTH
//#define LEO_VELOCITY_NONDIM LEO_VELOCITY / UNIT_VELOCITY
