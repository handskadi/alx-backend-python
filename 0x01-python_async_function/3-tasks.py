#!/usr/bin/env python3
"""
checking on th type of a return
"""
import asyncio


wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """the return type of a ascio.task"""
    task: asyncio.Task = asyncio.create_task(wait_random())
    return task
