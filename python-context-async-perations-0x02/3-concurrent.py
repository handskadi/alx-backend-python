import aiosqlite
import asyncio


async def async_fetch_users():
    result = []
    async with aiosqlite.connect('./../python-decorators-0x01/users.db') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            async for row in cursor:
                result.append(row)
    return result


async def async_fetch_older_users():
    result = []
    async with aiosqlite.connect('./../python-decorators-0x01/users.db') as db:

        async with db.execute("SELECT * FROM users where age > 40") as cursor:
            async for row in cursor:
                result.append(row)

    return result



async def fetch_concurrently():
    db_result = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print(db_result)

asyncio.run(fetch_concurrently())    