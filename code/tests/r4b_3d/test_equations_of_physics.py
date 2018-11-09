"""
Pytest module of corresponding python file without "test_" in the name.

To test of another function, simply:
1. Add tests to corresponding Mathematica script (run it to export JSON)
2. Import function in this module.
3. Copy the code block below (pytest decorator + test1) and
    3.1 Increment function name test[i+1]
    3.2 Put in function name string in:
        3.2.1 First argument to process_test_data()
        3.2.2 Docstring to test function

That's it!
"""
import json
import os
from pprint import pprint

import pytest

from orbsim.r4b_3d.equations_of_physics import (  # pylint: disable=W0611
    get_circular_orbit_speed,
    get_circular_orbit_period,
)


testdata_folder_path = os.path.dirname(os.path.realpath(__file__))
testdata_filename = os.path.basename(__file__).split(".")[0] + ".json"
testdata_file_path = testdata_folder_path + "/" + testdata_filename

with open(testdata_file_path) as file:
    test_data = json.load(file)


def process_test_data(function_name, input_type="list"):
    """
    Reformats JSON data to format suitable for @pytest.mark.parametrize decorator
    For example see https://docs.pytest.org/en/latest/parametrize.html.

    Arguments:
        function_name {str} -- Name of function to be tested.

    Keyword Arguments:
        output_type {str} -- Data in JSON will either be a single int/float or a list.
                             If 'tuple' is passed in, the list will be converted to a
                             tuple instead of a list. (default: {"unchanged"}).

    Returns:
        List[Tuple(Str, Any)] -- List of 2-tuples of function calls with input as
                                 strings and the expected output.
    """

    tests = test_data[function_name]

    function_tests = []
    for arg, output in tests:
        if input_type == "scalar":
            arg = tuple(arg)
        arg_str = str(arg)[1:-1]
        if not isinstance(output, str):
            # Make tuple list ("function(input)", output)
            function_tests.append((f"{function_name}({arg_str})", output))
        else:
            # Make pytest.param marked with xfail, e.g. pytest.param("6*9", 42, marks=pytest.mark.xfail)
            function_tests.append(
                pytest.param(
                    f"{function_name}({arg_str})",
                    None,
                    marks=pytest.mark.xfail(raises=ValueError),
                )
            )

    return function_tests


@pytest.mark.parametrize(
    "test_input, expected", process_test_data("get_circular_orbit_speed")
)
def test1(test_input, expected):
    """Test get_circular_orbit_speed"""
    assert eval(test_input) == pytest.approx(expected)  # pylint: disable=W0123


@pytest.mark.parametrize(
    "test_input, expected", process_test_data("get_circular_orbit_period")
)
def test2(test_input, expected):
    """Test get_circular_orbit_period"""
    assert eval(test_input) == pytest.approx(expected)  # pylint: disable=W0123


if __name__ == "__main__":
    func_name = "get_circular_orbit_speed"

    pprint(process_test_data(func_name, input_type="list"))
