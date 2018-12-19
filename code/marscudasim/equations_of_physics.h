#pragma once

#include "constants.h"
#include <math.h>

__host__ __device__
inline double get_circular_orbit_speed(double altitude)
{
    return sqrt(EARTH_MU / (EARTH_RADIUS + altitude));
}
