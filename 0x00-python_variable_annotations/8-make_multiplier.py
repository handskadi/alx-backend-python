#!/usr/bin/env python3
"""
type-annotated function make_multiplier that takes a
float multiplier as argument and returns a function
that multiplies a float by multiplier.
"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    make_multiplier is a function that returns another function:
    Callable[[float], float] hints that the function that we will
    return, takes an argument of type [float] and returns a float
    """
    def multiply(num: float):
        return num * multiplier

    return multiply
