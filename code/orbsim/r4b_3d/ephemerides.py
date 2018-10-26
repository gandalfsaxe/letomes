"""
Functions for getting celestial body positions (ephemerides).
These are used as input in equations of motions (analyticals.py) for distances to
various celestial bodies.
"""
import logging
import os
from math import floor

import pandas as pd

from orbsim.r4b_3d.logging import logging_setup

logging_setup()

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
    path_parts = os.path.realpath(__file__).split("/")[:-1]
    path_parts.append(relative_path)
    abs_path = "/".join(path_parts)

    os.chdir(abs_path)
    logging.debug(f"Current working directory: {os.getcwd()}")

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


def get_ephemerides_on_date(ephemerides, date=0):
    """
    Get ephemerides of all bodies in input for specific input day (continuous).
    --INPUT--
    ephemerides (DICT("body": pandas.df)):  Dict of ephemerides, from get_ephemerides()
    date (int or float):                    Days since 2019-01-01 00:00:00
    """
    day = date

    day_lower = floor(day)
    day_upper = day_lower + 1
    day_increment = day % 1

    interpolated_dict = {}

    for body, eph in ephemerides.items():

        start_position_df = eph.iloc[[day_lower]]
        end_position_df = eph.iloc[[day_upper]]

        start_position_series = start_position_df.iloc[0]
        end_position_series = end_position_df.iloc[0]

        diff_position_series = end_position_series - start_position_series

        interpolated_position = (
            start_position_series + day_increment * diff_position_series
        )

        interpolated_dict[body] = interpolated_position

    return interpolated_dict


if __name__ == "__main__":

    test_eph = get_ephemerides()
    logging.info(f"Ephemerides table:\n {test_eph}")

    test_date = 124.26
    test_eph_on_date = get_ephemerides_on_date(test_eph, test_date)
    logging.info(f"Ephemerides on date {test_date}:\n {test_eph_on_date}")
