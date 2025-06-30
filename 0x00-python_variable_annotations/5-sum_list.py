#!/usr/bin/env python3
"""
type-annotated function sum_list which takes a
list input_list of floats as argument and returns
their sum as a float.
"""
from typing import List


def sum_list(input_list: List[float]) -> float:
    """return the sum of all list elelments"""
    length: int
    sum: float
    length = len(input_list)
    sum = 0

    for i in range(length):
        sum += input_list[i]

    return sum
