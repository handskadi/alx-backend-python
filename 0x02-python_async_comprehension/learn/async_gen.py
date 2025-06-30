import asyncio

async def async_generator():
    yield "Hello"
    await asyncio.sleep(1)
    yield "World"

async def main():
    async for item in async_generator():
        print(item)

asyncio.run(main())
