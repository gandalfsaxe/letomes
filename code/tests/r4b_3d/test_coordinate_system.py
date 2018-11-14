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

from orbsim.r4b_3d.coordinate_system import (  # pylint: disable=W0611
    get_position_cartesian_from_spherical,
    get_position_spherical_from_cartesian,
    get_distance_cartesian,
    get_distance_spherical,
    get_velocity_spherical_from_cartesian,
    get_speed_cartesian,
    get_speed_spherical,
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
                                 strings and the expected test_output.
    """

    tests = test_data[function_name]

    function_tests = []
    for test_input, test_output in tests:
        if input_type == "scalar":
            test_input = tuple(test_input)  # should this be str(test_input) ?
        input_str = ", ".join(map(str, test_input))
        if not isinstance(test_output, str):
            # Expect success -> make tuple list ("function(input)", test_output)
            function_tests.append((f"{function_name}({input_str})", test_output))
        else:
            # Expect fail --> Make pytest.param marked with xfai
            # e.g. pytest.param("6*9", 42, marks=pytest.mark.xfail)
            function_tests.append(
                pytest.param(
                    f"{function_name}({input_str})",
                    None,
                    marks=pytest.mark.xfail(raises=ValueError),
                )
            )

    return function_tests


@pytest.mark.parametrize(
    "test_input, expected", process_test_data("get_position_cartesian_from_spherical")
)
def test1(test_input, expected):
    """Test get_position_cartesian_from_spherical"""
    assert eval(test_input) == pytest.approx(expected)  # pylint: disable=W0123


@pytest.mark.parametrize(
    "test_input, expected", process_test_data("get_position_spherical_from_cartesian")
)
def test2(test_input, expected):
    """Test get_position_spherical_from_cartesian"""
    assert eval(test_input) == pytest.approx(expected)  # pylint: disable=W0123


@pytest.mark.parametrize(
    "test_input, expected", process_test_data("get_distance_cartesian")
)
def test3(test_input, expected):
    """Test get_distance_cartesian"""
    assert eval(test_input) == pytest.approx(expected)  # pylint: disable=W0123


@pytest.mark.parametrize(
    "test_input, expected", process_test_data("get_distance_spherical")
)
def test4(test_input, expected):
    """Test get_distance_spherical"""
    assert eval(test_input) == pytest.approx(expected)  # pylint: disable=W0123


@pytest.mark.parametrize(
    "test_input, expected", process_test_data("get_distance_spherical")
)
def test5(test_input, expected):
    """Test get_distance_spherical"""
    assert eval(test_input) == pytest.approx(expected)  # pylint: disable=W0123


@pytest.mark.parametrize(
    "test_input, expected", process_test_data("get_velocity_spherical_from_cartesian")
)
def test6(test_input, expected):
    """Test get_velocity_spherical_from_cartesian"""
    assert eval(test_input) == pytest.approx(expected)  # pylint: disable=W0123


@pytest.mark.parametrize(
    "test_input, expected", process_test_data("get_speed_cartesian")
)
def test7(test_input, expected):
    """Test get_speed_cartesian"""
    assert eval(test_input) == pytest.approx(expected)  # pylint: disable=W0123


@pytest.mark.parametrize(
    "test_input, expected", process_test_data("get_speed_spherical")
)
def test8(test_input, expected):
    """Test get_speed_spherical"""
    assert eval(test_input) == pytest.approx(expected)  # pylint: disable=W0123


if __name__ == "__main__":
    func_name = "get_speed_spherical"

    pprint(process_test_data(func_name, input_type="scalar"))
