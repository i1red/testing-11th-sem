import math
from typing import Final

import pytest

from lab01.core.function import f


INVALID_ARGUMENT_HIGH: Final[float] = math.pi / 2 + 0.1
INVALID_ARGUMENT_LOW: Final[float] = -math.pi / 2 - 0.1
INVALID_PRECISION_HIGH: Final[float] = 1.
INVALID_PRECISION_LOW: Final[float] = 0.


def test_function_invalid_argument():
    with pytest.raises(ValueError):
        f(INVALID_ARGUMENT_HIGH, 1e-3)

    with pytest.raises(ValueError):
        f(INVALID_ARGUMENT_LOW, 1e-3)


def test_function_invalid_precision():
    with pytest.raises(ValueError):
        f(0., INVALID_PRECISION_HIGH)

    with pytest.raises(ValueError):
        f(0., INVALID_PRECISION_LOW)


@pytest.mark.parametrize(
    "argument,expected",
    [(0., 0.), (math.pi / 4, 0.3253225), (-math.pi / 4, -1.89611889)]
)
def test_function(argument: float, expected: float):
    actual = f(argument, 1e-3)
    assert (actual.value - expected) < 1e-3
