import json
import os

import pytest

from orbsim.analyticals import Pdot
from orbsim.constants import k


@pytest.fixture()
def math_data():

    math_json_filename = os.path.basename(__file__).split(".")[0] + ".json"

    with open(
        os.path.dirname(os.path.realpath(__file__)) + "/" + math_json_filename
    ) as file:
        data = json.load(file)
    return data


def test1_zeros(math_data):
    X = 0
    Y = 0
    Px = 0
    Py = 0
    assert Pdot(X, Y, Px, Py) == pytest.approx(math_data["test1"])


def test2_x_positive(math_data):
    X = 0.5
    Y = 0
    Px = 0
    Py = 0
    assert Pdot(X, Y, Px, Py) == pytest.approx(math_data["test2"])


def test3_y_negative(math_data):
    X = 0
    Y = -0.4
    Px = 0
    Py = 0
    assert Pdot(X, Y, Px, Py) == pytest.approx(math_data["test3"])


def test4_px_positive(math_data):
    X = 0
    Y = 0
    Px = 2
    Py = 0
    assert Pdot(X, Y, Px, Py) == pytest.approx(math_data["test4"])


def test5_py_negative(math_data):
    X = 0
    Y = 0
    Px = 0
    Py = -5
    assert Pdot(X, Y, Px, Py) == pytest.approx(math_data["test5"])


def test6_all_positive(math_data):
    X = 1
    Y = 2
    Px = 3
    Py = 4
    assert Pdot(X, Y, Px, Py) == pytest.approx(math_data["test6"])


def test7_all_negative(math_data):
    X = -4
    Y = -3
    Px = -2
    Py = -1
    assert Pdot(X, Y, Px, Py) == pytest.approx(math_data["test7"])


def test8_all_mixed(math_data):
    X = -1
    Y = 1
    Px = -3
    Py = 4
    assert Pdot(X, Y, Px, Py) == pytest.approx(math_data["test8"])
