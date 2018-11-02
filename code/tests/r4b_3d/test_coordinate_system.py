"""Pytest for R3B-2D equations, e.g. pdot_x and pdot_y. Note that x and y are so simple
that they need not be tested.

To test of another function, simply add it to corresponding Mathematica script and copy
The decorator + test function below and change the first string argument to
process_test_data() and docstring. That's it!
"""
import json
import os

import pytest

from orbsim.r4b_3d.coordinate_system import (  # pylint: disable=W0611
    get_position_cartesian_from_spherical,
)


testdata_folder_path = os.path.dirname(os.path.realpath(__file__))
testdata_filename = os.path.basename(__file__).split(".")[0] + ".json"
testdata_file_path = testdata_folder_path + "/" + testdata_filename

with open(testdata_file_path) as file:
    test_data = json.load(file)


def process_test_data(function_name, output_type="unchanged"):
    """
    Reformats JSON data to format suitable for @pytest.mark.parametrize decorator
    For example see https://docs.pytest.org/en/latest/parametrize.html.

    Arguments:
        function_name {str} -- Name of function to be tested.

    Keyword Arguments:
        output_type {str} -- Data in JSON will either be a single int/float or a list.
                             If 'tuple' is passed in, the list will be converted to a
                             tuple instead. (default: {"unchanged"}).

    Returns:
        List[Tuple(Str, Any)] -- List of 2-tuples of function calls with input as
                                 strings and the expected output.
    """

    tests = test_data[function_name]

    function_tests = []
    for arg, output in tests:
        arg_str = ", ".join(map(str, arg))
        if output_type == "tuple":
            output = tuple(output)
        function_tests.append((f"{function_name}({arg_str})", output))

    return function_tests


@pytest.mark.parametrize(
    "test_input, expected",
    process_test_data("get_position_cartesian_from_spherical", output_type="tuple"),
)
def test1(test_input, expected):
    """Test get_position_cartesian_from_spherical"""
    assert eval(test_input) == pytest.approx(expected)  # pylint: disable=W0123
