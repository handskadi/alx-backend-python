#!/usr/bin/env python3
"""
a coroutine that takes no arguments
"""
from typing import AsyncGenerator, List
import random
import asyncio


async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """
    writing an async comprehension that collects
    10 random numbers
    """
    return [result async for result in async_generator()][:10]
