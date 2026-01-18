import aiosqlite
from contextlib import asynccontextmanager


class Database:
    def __init__(self, path: str):
        self.path = path
        self._initialized = False

    @asynccontextmanager
    async def connect(self):
        conn = await aiosqlite.connect(self.path)
        conn.row_factory = aiosqlite.Row
        try:
            yield conn
            await conn.commit()
        finally:
            await conn.close()

    async def execute(self, sql: str, params: tuple = ()):
        async with self.connect() as conn:
            await conn.execute(sql, params)

    async def fetchall(self, sql: str, params: tuple = ()):
        async with self.connect() as conn:
            cursor = await conn.execute(sql, params)
            return await cursor.fetchall()


db = Database("db.sqlite3")
