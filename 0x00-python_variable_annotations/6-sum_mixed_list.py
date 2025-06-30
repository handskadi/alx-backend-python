#!/usr/bin/env python3
"""
ype-annotated function sum_mixed_list which takes
a list mxd_lst of integers and floats and returns their
sum as a float.
"""
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """summing a mixed list"""
    length: int
    sum: float

    length = len(mxd_lst)
    sum = 0

    for i in range(length):
        sum += mxd_lst[i]

    return sum
