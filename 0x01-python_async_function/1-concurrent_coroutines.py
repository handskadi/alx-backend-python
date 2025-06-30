#!/usr/bin/env python3
"""
executing multiple coroutines at the same time with async
"""
from typing import List
import asyncio
import random


wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """spwan wait_random n times and return the list"""
    tasks = []

    for _ in range(n):
        tasks.append(asyncio.create_task(wait_random(max_delay)))
    all: List[float] = sorted(await asyncio.gather(*tasks))
    return all
