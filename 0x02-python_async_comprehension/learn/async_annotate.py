import asyncio
from typing import AsyncGenerator

async def async_generator() -> AsyncGenerator[str, None]:
    yield "Hello"
    await asyncio.sleep(1)
    yield "World"

async def main():
    async for item in async_generator():
        print(item)

asyncio.run(main())
