#!/usr/bin/env python3
"""
type-annotated function floor which takes a float n as
argument and returns the floor of the float.
"""
import math


def floor(n: float) -> int:
    """
    return the largest integer that is less that or equal to the float value
    """
    return math.floor(n)
