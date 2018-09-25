"""
Functions for getting celestial body positions (ephemerides).
These are used as input in equations of motions (analyticals.py) for distances to
various celestial bodies.
"""
import os

import pandas as pd


def get_ephemerides(
    relative_path="ephemerides/",
    planets=("earth", "mars"),
    end_year="2020",
    interpolation=9,
):
    """
    --INPUT--
    relative_path (str):            relative path of ephemerides files (to this script)
    planets TUP(str):              list of planets to include
    end_year (str):                 end_year-01-01 will be last date in ephemerides.
    interpolation (Boolean or int): number of interpolation points between two days

    --OUTOUT--:
    ephemerides (DICT("body": pandas.df))
    """

    # Input value checks
    VALID_planets = ["earth", "mars"]
    VALID_END_YEARS = ["2020", "2039", "2262"]
    VALID_INTERPOLATION_POINTS = [9]

    for planet in planets:
        if planet not in VALID_planets:
            raise ValueError(
                "planets contain invalid planets (valid: 'earth' and 'mars')"
            )

    if end_year not in VALID_END_YEARS:
        raise ValueError("Invalid end year. Must be '2020', '2039' or '2262'.")

    if interpolation not in VALID_INTERPOLATION_POINTS:
        raise ValueError("Invalid INTERPOLATION_POINTS. Must be 9.")

    # Change workdir, construct filenames

    path_parts = os.path.realpath(__file__).split("/")[:-1]
    path_parts.append(relative_path)
    abs_path = "/".join(path_parts)

    os.chdir(abs_path)
    # cwd = os.getcwd()
    # print(cwd)

    if interpolation:
        extrapolated_filename_element = "_extrapolated-{}".format(interpolation)
    else:
        extrapolated_filename_element = ""

    ephemerides_filename_dict = {}

    for planet in planets:
        ephemerides_filename_dict[planet] = "{}_2019-{}{}.csv".format(
            planet, end_year, extrapolated_filename_element
        )
    # print(ephemerides_filename_dict)

    # Import csv files into dict

    # Read CSV files into dict
    ephemerides = {}
    for body, csv_filename in ephemerides_filename_dict.items():
        imported_body = pd.read_csv(csv_filename, parse_dates=["date"], index_col="day")
        imported_body.insert(
            0, "day", imported_body.index
        )  # 'day' also as first column
        ephemerides[body] = imported_body
    # print(ephemerides)

    return ephemerides


def get_ephemerides_on_date(ephemerides, date=0):
    """
    Get ephemerides of all bodies in input for specific date.
    --INPUT--
    ephemerides (DICT("body": pandas.df)):  Dict of ephemerides, from get_ephemerides()
    date (int or float):                    Days since 2019-01-01 00:00:00
    """
    ephemerides_at_date_dict = {}

    for body, eph in ephemerides.items():
        # date is day (day=0 at 2019-01-01 00:00:00)
        if isinstance(date, int) or isinstance(date, float):
            try:
                result = eph.loc[date]
            except KeyError:
                closest_date = eph.index.get_loc(date, method="nearest")
                print(
                    "Date = {} rounded to date = {} (index = {})".format(
                        date, eph.iloc[closest_date]["day"], closest_date
                    )
                )
                print(eph.iloc[closest_date])
            else:
                print("Exact index found at date = {}".format(date))
                print(eph.loc[date])
        else:
            raise ValueError(
                "Date must be day in float or int (day=0 at 2019-01-01 00:00:00)"
            )  # TODO: Implement support for datetime / Timestamp

        ephemerides_at_date_dict[body] = result

    return ephemerides_at_date_dict


if __name__ == "__main__":
    test_eph = get_ephemerides()
    print(test_eph)

    test_eph_on_date = get_ephemerides_on_date(test_eph, 124.2)
    print(test_eph_on_date)
