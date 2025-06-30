#!/usr/bin/env python3
"""
measuring the runtime of a coroutine
"""
from typing import List
import time
import asyncio


async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
    we are executing the async comprehension using asyncio.gather
    """
    tasks: List[asyncio.Task] = []
    start: float = time.time()
    for _ in range(4):
        task: asyncio.Task = asyncio.create_task(async_comprehension())
        tasks.append(task)

    finals: List[List[float]] = await asyncio.gather(*tasks)
    end: float = time.time()

    runtime: float = end - start
    return runtime
