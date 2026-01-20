from orm.db import db

from typing import TYPE_CHECKING, Optional, AsyncGenerator

if TYPE_CHECKING:
    from orm.model import ModelMeta


class QuerySet:
    """
    Ленивая асинхронная выборка объектов модели.

    Представляет собой описание запроса, а не результат его выполнения.
    """
    def __init__(self, model: 'ModelMeta', where: Optional[list] = None, params: Optional[list] = None):
        self.model = model
        self.where = list(where or [])
        self.params = list(params or [])

    def filter(self, **kwargs) -> 'QuerySet':
        where = list(self.where)
        params = list(self.params)
        for k, v in kwargs.items():
            where.append(f"{k} = ?")
            params.append(v)
        return QuerySet(self.model, where=where, params=params)

    def _where_clause(self) -> str:
        """Формирует SQL-фрагмент WHERE для текущей выборки"""

        if self.where:
            return "WHERE " + " AND ".join(self.where)
        return ""

    async def all(self) -> list:
        where = self._where_clause()
        sql = f"SELECT * FROM {self.model._table} {where}"
        rows = await db.fetchall(sql, tuple(self.params))
        return [self.model(**dict(r)) for r in rows]

    def __aiter__(self) -> AsyncGenerator:
        """Поддержка асинхронной итерации по результатам выборки"""

        async def gen():
            for obj in await self.all():
                yield obj

        return gen()

    async def get(self, **kwargs) -> ModelMeta:
        qs = self.filter(**kwargs)
        where = qs._where_clause()
        sql = f"SELECT * FROM {qs.model._table} {where} LIMIT 2"
        rows = await db.fetchall(sql, tuple(qs.params))
        if not rows:
            raise ValueError("Object does not exist")
        if len(rows) > 1:
            raise ValueError("Multiple objects returned")
        return qs.model(**dict(rows[0]))

    async def delete(self):
        where = self._where_clause()
        sql = f"DELETE FROM {self.model._table} {where}"
        await db.execute(sql, tuple(self.params))

    async def exists(self) -> bool:
        where = self._where_clause()
        sql = f"SELECT 1 FROM {self.model._table} {where} LIMIT 1"
        rows = await db.fetchall(sql, tuple(self.params))
        return len(rows) > 0
