import aiosqlite
from contextlib import asynccontextmanager


class Database:
    """
    Обертка над aiosqlite.
    Обеспечивает автоматическое управление соединением.

    Не реализует пул соединений.
    """
    def __init__(self, path: str):
        self.path = path
        self._initialized = False

    @asynccontextmanager
    async def connect(self):
        """
        Асинхронный контекстный менеджер соединения с БД.

        Предназначен для краткоживущих операций.
        """
        conn = await aiosqlite.connect(self.path)
        conn.row_factory = aiosqlite.Row
        try:
            yield conn
            await conn.commit()
        finally:
            await conn.close()

    async def execute(self, sql: str, params: tuple = ()):
        """Выполняет SQL-запрос без возврата данных"""

        async with self.connect() as conn:
            await conn.execute(sql, params)

    async def fetchall(self, sql: str, params: tuple = ()):
        """Выполняет SQL-запрос и возвращает все строки результата"""

        async with self.connect() as conn:
            cursor = await conn.execute(sql, params)
            return await cursor.fetchall()


db = Database("db.sqlite3")
