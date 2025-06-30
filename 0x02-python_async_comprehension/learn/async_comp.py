import asyncio

async def async_function(i):
    await asyncio.sleep(i)
    return i

async def main():
    results = [await async_function(i) for i in range(1, 6)]
    print(results)

asyncio.run(main())
