import asyncio

async def fetch_data():
    print("start fetching")
    await asyncio.sleep(2)
    print("done fetching")
    return {"data": 1}

async def print_numbers():
    for i in range(10):
        print(i)
        await asyncio.sleep(0.25)

async def main():
    #starting both task.
    task1 = asyncio.create_task(fetch_data()) #this creates a future - there could be  value that may be returned
    task2 = asyncio.create_task(print_numbers())

    #waiting for task one to finish before we continue
    value1 = await task1 #its return value is now stored in value1 - its future
    print(value1)
    #wait for task two to finish
    await task2


asyncio.run(main())