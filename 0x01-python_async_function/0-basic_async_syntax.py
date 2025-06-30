#!/usr/bin/env python3
"""
an asynchronous couritine that takes in an in
"""
import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """random delay betweeen 0 and max delay and return it"""
    delay: float = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
