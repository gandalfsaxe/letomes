import json
import os

import pytest

from orbsim.r3b_2d import k
from orbsim.r3b_2d.analyticals import get_pdot_x, get_pdot_y, pdot_denominators


@pytest.fixture()
def math_data():

    math_json_filename = os.path.basename(__file__).split(".")[0] + ".json"

    with open(
        os.path.dirname(os.path.realpath(__file__)) + "/" + math_json_filename
    ) as file:
        data = json.load(file)
    return data


def test1_zeros(math_data):
    x = 0
    y = 0
    p_x = 0
    p_y = 0
    assert [get_pdot_x(x, y, p_y), get_pdot_y(x, y, p_x)] == pytest.approx(
        math_data["test1"]
    )


def test2_x_positive(math_data):
    x = 0.5
    y = 0
    p_x = 0
    p_y = 0
    assert [get_pdot_x(x, y, p_y), get_pdot_y(x, y, p_x)] == pytest.approx(
        math_data["test2"]
    )


def test3_y_negative(math_data):
    x = 0
    y = -0.4
    p_x = 0
    p_y = 0
    assert [get_pdot_x(x, y, p_y), get_pdot_y(x, y, p_x)] == pytest.approx(
        math_data["test3"]
    )


def test4_px_positive(math_data):
    x = 0
    y = 0
    p_x = 2
    p_y = 0
    assert [get_pdot_x(x, y, p_y), get_pdot_y(x, y, p_x)] == pytest.approx(
        math_data["test4"]
    )


def test5_py_negative(math_data):
    x = 0
    y = 0
    p_x = 0
    p_y = -5
    assert [get_pdot_x(x, y, p_y), get_pdot_y(x, y, p_x)] == pytest.approx(
        math_data["test5"]
    )


def test6_all_positive(math_data):
    x = 1
    y = 2
    p_x = 3
    p_y = 4
    assert [get_pdot_x(x, y, p_y), get_pdot_y(x, y, p_x)] == pytest.approx(
        math_data["test6"]
    )


def test7_all_negative(math_data):
    x = -4
    y = -3
    p_x = -2
    p_y = -1
    assert [get_pdot_x(x, y, p_y), get_pdot_y(x, y, p_x)] == pytest.approx(
        math_data["test7"]
    )


def test8_all_mixed(math_data):
    x = -1
    y = 1
    p_x = -3
    p_y = 4
    assert [get_pdot_x(x, y, p_y), get_pdot_y(x, y, p_x)] == pytest.approx(
        math_data["test8"]
    )
