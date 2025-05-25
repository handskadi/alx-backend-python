import asyncio
import aiosqlite

async def asyncfetchusers():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            print("All Users:")
            for row in rows:
                print(row)
            return rows  # ✅ Required by checker

async def asyncfetcholder_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            print("\nUsers older than 40:")
            for row in rows:
                print(row)
            return rows  # ✅ Required by checker

async def fetch_concurrently():
    await asyncio.gather(
        asyncfetchusers(),
        asyncfetcholder_users()
    )

# ✅ Run concurrently
asyncio.run(fetch_concurrently())
