"""
All physics equations not related to Hamilton's equations (equations of motion).

- Closed circular
    - orbital speed
    - period
"""

from math import pi, sqrt

import logging

from orbsim import EARTH_RADIUS, MARS_RADIUS, SUN_RADIUS
from orbsim.r4b_3d import EARTH_MU, MARS_MU, SUN_MU, UNIT_LENGTH, UNIT_TIME

# from orbsim.r4b_3d.coordinate_system import (
#     get_position_spherical_from_cartesian,
#     get_speed_spherical,
#     get_velocity_spherical_from_cartesian,
# )
# from orbsim.r4b_3d.ephemerides import get_ephemerides, get_ephemerides_on_day

# region Circular Orbit
def get_circular_orbit_speed(body="Earth", altitude=160):
    """ Get speed of LEO (Low Earth Orbit) at designated altitude.

    Keyword Arguments:
        altitude {int} -- distance above Earth surface in km (default: {160})

    Returns:
        [int] -- speed in km/s.
    """

    if body == "Sun":
        mu = SUN_MU
        radius = SUN_RADIUS
    elif body == "Earth":
        mu = EARTH_MU
        radius = EARTH_RADIUS
    elif body == "Mars":
        mu = MARS_MU
        radius = MARS_RADIUS

    v = sqrt(mu / (radius + altitude))

    v_au_y = v / (UNIT_LENGTH / UNIT_TIME)

    logging.debug(
        f"Circular orbital speed around {body} at {altitude} km altitude (km/s): {v}"
        f" (Initial 160 km LEO expected speed: 7.812 km/s (via Wolfram Alpha))"
        # https://www.wolframalpha.com/input/?i=7.812+km%2Fs+in+au%2Fy
    )
    logging.debug(
        f"Circular orbital speed around {body} at {altitude} km altitude (AU/y):"
        f" {v_au_y}"
        f" (Initial 160 km LEO expected speed: 1.6468 au/y (via Wolfram Alpha))"
        # https://www.wolframalpha.com/input/?i=circular+orbital+speed+earth+altitude+160km
    )

    return v


def get_circular_orbit_period(body="Earth", altitude=160):
    """ Get period of LEO (Low Earth Orbit) at designated altitude.

    Keyword Arguments:
        altitude {int} -- distance above Earth surface in km (default: {160})

    Returns:
        [int] -- period in s.
    """

    if body == "Sun":
        mu = SUN_MU
        radius = SUN_RADIUS
    elif body == "Earth":
        mu = EARTH_MU
        radius = EARTH_RADIUS
    elif body == "Mars":
        mu = MARS_MU
        radius = MARS_RADIUS

    T = 2 * pi * sqrt((radius + altitude) ** 3 / (mu))

    T_y = T * UNIT_TIME

    logging.debug(
        f"Circular orbital period around {body} at {altitude} km altitude (s): {T}"
        f" (Initial 160 km LEO expected period: 5261 s (via Wolfram Alpha)"
    )
    # https://www.wolframalpha.com/input/?i=circular+orbital+period+earth+altitude+160km

    logging.debug(
        f"Circular orbital period around {body} at {altitude} km altitude (h): {T_y}"
        f" (Initial 160 km LEO expected period: 1.461 h  (Via Wolfram Alpha)"
    )
    # https://www.wolframalpha.com/input/?i=circular+orbital+period+earth+altitude+160km

    return T


# endregion


if __name__ == "__main__":

    get_circular_orbit_speed()

    get_circular_orbit_period()
