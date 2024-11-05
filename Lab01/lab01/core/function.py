import math
from functools import cache

import sympy

from lab01.core.result import Result


def f(x: float, e: float) -> Result:
    if abs(x) >= math.pi / 2:
        raise ValueError("x should be in range (-pi / 2, pi / 2)")

    if not 0. < e < 1.:
        raise ValueError("e should be in range (0, 1)")

    value = x * _sec_k(x, 0)
    k = 1

    while True:
        term = x * (_sec_k(x, k) - _tan_k(x, k))
        value += term

        k += 1

        if abs(term) <= e:
            break

    return Result(argument=x, precision=e, value=value, n_terms=k)

@cache
def _factorial(n):
    if n == 0:
        return 1

    return n * _factorial(n - 1)


def _sec_k(x: float, k: int) -> float:
    sign = 1 if k % 2 == 0 else -1
    coefficient = sympy.euler(2 * k) / _factorial(2 * k)
    x_k = x ** (2 * k)
    return sign * coefficient * x_k


def _tan_k(x: float, k: int) -> float:
    sign = 1 if k % 2 == 0 else -1
    coefficient = sympy.bernoulli(2 * k) * (4 ** k) * (1 - 4 ** k) / _factorial(2 * k)
    x_k = x ** (2 * k - 1)
    return sign * coefficient * x_k
