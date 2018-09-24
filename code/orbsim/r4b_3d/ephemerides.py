"""
Functions for getting planets positions (ephemeris).
Will either get done via table or simulated elliptical orbits, whichever proves easier.
"""
import os

import pandas as pd


# Paths and files

RELATIVE_PATH = "ephemerides/"  # relative path of ephemerides files (to this script)

EPHEMERIDES_2039_DICT = {"earth": "earth_2019-2039.csv", "mars": "mars_2019-2039.csv"}

EPHEMERIDES_2262_DICT = {"earth": "earth_2019-2262.csv", "mars": "mars_2019-2262.csv"}

# Change working dir

path_parts = os.path.realpath(__file__).split("/")[:-1]
path_parts.append("ephemerides/")
abs_path = "/".join(path_parts)

os.chdir(abs_path)
cwd = os.getcwd()
# print(cwd)


# Something


def get_ephemerides(date=0, end_year=2039):

    if end_year == 2039:
        FILENAME_DICT = EPHEMERIDES_2039_DICT
    elif end_year == 2262:
        FILENAME_DICT = EPHEMERIDES_2262_DICT
    else:
        raise ValueError("Not a valid end-year for ephemerides (must be 2039 or 2262)")

    earth = pd.read_csv(FILENAME_DICT["earth"], parse_dates=["date"], index_col="days")
    mars = pd.read_csv(FILENAME_DICT["mars"], parse_dates=["date"], index_col="days")

    return earth.loc[date], mars.loc[date]


print(get_ephemerides(10))
