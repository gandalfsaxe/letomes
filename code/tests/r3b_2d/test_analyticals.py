"""Pytest for R3B-2D equations, e.g. pdot_x and pdot_y. Note that x and y are so simple
that they need not be tested.
"""
import json
import os

import pytest

from orbsim.r3b_2d.analyticals import get_pdot_x, get_pdot_y


def math_data():
    """import data from json file created by mathematica script and import as
    'ground truth'
    """

    math_json_filename = os.path.basename(__file__).split(".")[0] + ".json"

    with open(
        os.path.dirname(os.path.realpath(__file__)) + "/" + math_json_filename
    ) as file:
        data = json.load(file)
    return data


def test1_zeros():
    """Test 1"""
    data = math_data()
    x = 0
    y = 0
    p_x = 0
    p_y = 0
    assert [get_pdot_x(x, y, p_y), get_pdot_y(x, y, p_x)] == pytest.approx(
        data["test1"]
    )


def test2_x_positive():
    """Test 2"""
    data = math_data()
    x = 0.5
    y = 0
    p_x = 0
    p_y = 0
    assert [get_pdot_x(x, y, p_y), get_pdot_y(x, y, p_x)] == pytest.approx(
        data["test2"]
    )


def test3_y_negative():
    """Test 3"""
    data = math_data()
    x = 0
    y = -0.4
    p_x = 0
    p_y = 0
    assert [get_pdot_x(x, y, p_y), get_pdot_y(x, y, p_x)] == pytest.approx(
        data["test3"]
    )


def test4_px_positive():
    """Test 4"""
    data = math_data()
    x = 0
    y = 0
    p_x = 2
    p_y = 0
    assert [get_pdot_x(x, y, p_y), get_pdot_y(x, y, p_x)] == pytest.approx(
        data["test4"]
    )


def test5_py_negative():
    """Test 5"""
    data = math_data()
    x = 0
    y = 0
    p_x = 0
    p_y = -5
    assert [get_pdot_x(x, y, p_y), get_pdot_y(x, y, p_x)] == pytest.approx(
        data["test5"]
    )


def test6_all_positive():
    """Test 6"""
    data = math_data()
    x = 1
    y = 2
    p_x = 3
    p_y = 4
    assert [get_pdot_x(x, y, p_y), get_pdot_y(x, y, p_x)] == pytest.approx(
        data["test6"]
    )


def test7_all_negative():
    """Test 7"""
    data = math_data()
    x = -4
    y = -3
    p_x = -2
    p_y = -1
    assert [get_pdot_x(x, y, p_y), get_pdot_y(x, y, p_x)] == pytest.approx(
        data["test7"]
    )


def test8_all_mixed():
    """Test 8"""
    data = math_data()
    x = -1
    y = 1
    p_x = -3
    p_y = 4
    assert [get_pdot_x(x, y, p_y), get_pdot_y(x, y, p_x)] == pytest.approx(
        data["test8"]
    )
