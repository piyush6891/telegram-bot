import asyncpg
import os

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            os.getenv("DATABASE_URL"),
            min_size=5,
            max_size=20
        )

    async def setup(self):
        async with self.pool.acquire() as conn:
            await conn.execute("""
            CREATE TABLE IF NOT EXISTS members(
                user_id BIGINT PRIMARY KEY,
                username TEXT,
                balance INT DEFAULT 0,
                invites INT DEFAULT 0,
                invited_by BIGINT
            )
            """)

    async def add_user(self, uid, username, inviter=None):
        async with self.pool.acquire() as conn:
            await conn.execute("""
            INSERT INTO members(user_id,username,invited_by)
            VALUES($1,$2,$3)
            ON CONFLICT (user_id) DO NOTHING
            """, uid, username, inviter)

            if inviter:
                await conn.execute("""
                UPDATE members
                SET invites=invites+1
                WHERE user_id=$1
                """, inviter)

    async def get_user(self, uid):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(
                "SELECT * FROM members WHERE user_id=$1", uid
            )

    async def add_balance(self, uid, amt):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "UPDATE members SET balance=balance+$1 WHERE user_id=$2",
                amt, uid
            )

db = Database()
