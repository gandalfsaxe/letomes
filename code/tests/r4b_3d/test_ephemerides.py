"""
Pytest module of corresponding python file without "test_" in the name.
"""
import json
import os

import pytest

from orbsim.r4b_3d.ephemerides import get_ephemerides, get_ephemerides_on_day


def import_expected(function: str):
    """import data from json file created by mathematica script and import as
    'ground truth'
    """

    math_json_filename = os.path.basename(__file__).split(".")[0] + ".json"

    with open(
        os.path.dirname(os.path.realpath(__file__)) + "/" + math_json_filename
    ) as file:
        data = json.load(file)

    return data[function]


def filter_expected(function_name: str, data):
    xsuccess = []
    xfail = []

    for test_input, test_output in data:

        input_str = str(test_input)

        if isinstance(test_output, str):
            # Expect fail --> Make pytest.param marked with xfai
            # e.g. pytest.param("6*9", 42, marks=pytest.mark.xfail)
            xfail.append(
                pytest.param(
                    f"{function_name}(ephemerides,{input_str})",
                    None,
                    marks=pytest.mark.xfail(raises=ValueError),
                )
            )

        else:
            # Expect success -> make tuple list ("function(input)", test_output)
            eph = get_ephemerides_on_day(get_ephemerides(), test_input)
            earth = list(eph["earth"])
            mars = list(eph["mars"])

            del earth[2]
            del mars[2]

            xsuccess.append(([earth, mars], test_output))

    return xsuccess, xfail


test_data_list = import_expected("get_ephemerides_on_day")
xsuccess, xfail = filter_expected("get_ephemerides_on_day", test_data_list)


@pytest.mark.parametrize("test_input, expected", xfail)
def test_invalid_days(test_input, expected):
    """
    Tests of get_ephemerides_on_day"""

    # 1. We have to use pytest.approx since there is a difference on the rounding of the
    #    very last decimal in reading in the .csv between Python and Mathematica.

    # 2. We have to iterate over the input/output with for loop since pytest.approx does
    #    not support nested structures.

    ephemerides = get_ephemerides()  # pylint: disable=W0612
    assert eval(test_input) == expected  # pylint: disable=W0123


@pytest.mark.parametrize("test_input, expected", xsuccess)
def test_valid_days(test_input, expected):
    """
    Tests of get_ephemerides_on_day"""

    # 1. We have to use pytest.approx since there is a difference on the rounding of the
    #    very last decimal in reading in the .csv between Python and Mathematica.

    # 2. We have to iterate over the input/output with for loop since pytest.approx does
    #    not support nested structures.

    for i, test_input_part in enumerate(test_input):
        assert test_input_part == pytest.approx(expected[i])


@pytest.mark.xfail(strict=True, raises=ValueError)
def test_invalid_planets():
    """Tests of get_ephemerides (INVALID PLANETS)"""

    get_ephemerides(planets=("earth", "mercury"))


@pytest.mark.xfail(raises=ValueError)
def test_invalid_end_year():
    """Tests of get_ephemerides (INVALID YEARS)"""

    get_ephemerides(end_year="2042")


# if __name__ == "__main__":

#     imported_data = import_expected("get_ephemerides_on_day")
#     xs, xf = filter_expected("get_ephemerides_on_day", imported_data)

#     x = 2

