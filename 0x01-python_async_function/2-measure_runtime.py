#!/usr/bin/env python3
"""
measuring the run time
"""
import asyncio
import random
import time


wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """executing an asynchronous function in a non one"""
    start: float = time.time()
    asyncio.run(wait_n(n, max_delay))
    stop: float = time.time()

    total_time: float = (stop - start) / n
    return total_time
