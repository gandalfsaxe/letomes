"""
Functions for getting celestial body positions (ephemerides).
These are used as input in equations of motions (analyticals.py) for distances to
various celestial bodies.
"""
import logging
import os
from math import floor, pi

import pandas as pd

from orbsim.r4b_3d.logging import logging_setup
from orbsim.r4b_3d import SUN_R, SUN_PHI, SUN_THETA

logger = logging.getLogger()


def get_ephemerides(
    relative_path="ephemerides/", planets=("earth", "mars"), end_year="2020"
):
    """ Get table of ephemerides for all specified bodies from 2019-01-01 00:00:00 until
    01-01 00:00:00 of the end year.

    Note that the raw ephemerides files (e.g. `horizons_results_earth_2019-2020.txt`)
    are converted into the pre-processed files (e.g. `earth_2019-2020.csv`) by notebook
    `eph-import.ipynb`, downloaded from URL https://ssd.jpl.nasa.gov/horizons.cgi
    , with settings as described in `ssd-jpl-horizon-settings.md`.

    --INPUT--
    relative_path (str):            relative path of ephemerides files (to this script)
    planets TUP(str):               list of planets to include
    end_year (str):                 end_year-01-01 will be last date in ephemerides.

    --OUTOUT--:
    ephemerides (DICT("body": pandas.df))
    """

    # Input value checks
    VALID_planets = ["earth", "mars"]
    VALID_END_YEARS = ["2020", "2039", "2262"]

    for planet in planets:
        if planet not in VALID_planets:
            raise ValueError(
                "Planets contain invalid planets (valid: 'earth' and 'mars')"
            )

    if end_year not in VALID_END_YEARS:
        raise ValueError("Invalid end year. Must be '2020', '2039' or '2262'.")

    # Change workdir, construct filenames
    relative_path = os.path.normcase(relative_path)
    path_parts = os.path.realpath(__file__).split(os.path.normcase("/"))[:-1]
    path_parts.append(relative_path)
    abs_path = "/".join(path_parts)

    os.chdir(abs_path)
    # logging.debug(f"Current working directory: {os.getcwd()}")

    ephemerides_filename_dict = {}

    for planet in planets:
        ephemerides_filename_dict[planet] = f"{planet}_2019-{end_year}.csv"

    # Read CSV files into dict
    ephemerides = {}
    for body, csv_filename in ephemerides_filename_dict.items():
        imported_body = pd.read_csv(csv_filename, parse_dates=["date"], index_col="day")
        imported_body.insert(
            0, "day", imported_body.index
        )  # 'day' also as first column
        ephemerides[body] = imported_body

    return ephemerides


def get_ephemerides_on_day(ephemerides, day_index=0):
    """
    Get ephemerides of all bodies in input for specific input day (continuous).
    --INPUT--
    ephemerides (DICT("body": pandas.df)):  Dict of ephemerides, from get_ephemerides()
    date (int or float):                    Days since 2019-01-01 00:00:00
    """

    # Check for day out of bounds with respect to the imported ephemerides
    max_day_index = len(ephemerides["earth"]) - 2

    if day_index < -1 or day_index > max_day_index:  # +2 due to starting on day=-1
        raise ValueError(f"Day out of bounds, must be in interval [-1,{max_day_index}]")

    day = day_index + 1  # Since day starts at -1, only used for velocity estimation

    day_lower = floor(day)
    day_upper = day_lower + 1
    day_increment = day % 1

    eph_on_day = {}

    for body, eph in ephemerides.items():

        start_position_df = eph.iloc[[day_lower]]
        end_position_df = eph.iloc[[day_upper]]

        start_position_series = start_position_df.iloc[0]
        end_position_series = end_position_df.iloc[0]

        diff_position_series = end_position_series - start_position_series

        interpolated_position = (
            start_position_series + day_increment * diff_position_series
        )

        eph_on_day[body] = interpolated_position

    sun = eph_on_day["earth"].copy()
    sun["r"] = SUN_R
    sun["theta"] = SUN_THETA
    sun["phi"] = SUN_PHI
    sun["x"] = 0
    sun["y"] = 0
    sun["z"] = 0

    eph_on_day["sun"] = sun

    return eph_on_day


def get_coordinates_on_day_rad(ephemerides_on_day):
    """Take in ephemerides object in form af a Pandas.Series and extract just the
    coordinates, both cartesian and spherical.

    Arguments:
        ephemerides_on_day {Pandas.Series} -- Ephemerides table output from function
                                              ephemerides_on_day().

    Returns:
        Tuple(List(float)) -- Coordinates in both cartesian and spherical format in list
                              [r,theta,phi,x,y,z] in a coordinate tuple
                              (sun, earth, mars)
    """

    R_ks = []
    theta_ks = []
    phi_ks = []

    for body in ["sun", "earth", "mars"]:
        R_ks.append(ephemerides_on_day[body]["r"])
        theta_ks.append(ephemerides_on_day[body]["theta"] * pi / 180)
        phi_ks.append(ephemerides_on_day[body]["phi"] * pi / 180)

    return R_ks, theta_ks, phi_ks


# if __name__ == "__main__":

#     from pprint import pprint

#     test = get_coordinates_on_day_rad(get_ephemerides_on_day(get_ephemerides(), 0))

#     pprint(test)

#     pass

#     # # test_date = 124.26
#     # test_day = 0
#     # test_eph_on_day = get_ephemerides_on_day(test_eph, test_day)

#     # logging.info(f"Ephemerides on day {test_day}:\n {test_eph_on_day}")
