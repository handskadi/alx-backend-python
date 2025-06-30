#!/usr/bin/env python3
"""
Annotate the function parameters and return values with the appropriate types
"""
from typing import Tuple, List, Sequence, Iterable


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """ducky typing they call it"""
    return [(i, len(i)) for i in lst]
