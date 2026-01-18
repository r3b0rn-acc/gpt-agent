import importlib
import pkgutil
from typing import Iterable

from orm.db import db
from orm.fields import Field
from orm.query import QuerySet


_MODEL_REGISTRY = {}


def register_model(cls) -> None:
    _MODEL_REGISTRY[cls.__name__] = cls


def get_registered_models() -> list:
    return list(_MODEL_REGISTRY.values())


def autodiscover_models(package_name: str = "models") -> None:
    package = importlib.import_module(package_name)
    for _, module_name, _ in pkgutil.iter_modules(
        package.__path__, package.__name__ + "."
    ):
        importlib.import_module(module_name)


async def create_tables(models: Iterable[type] | None = None) -> None:
    for model in models or get_registered_models():
        await model._create_table()


async def init_models(package_name: str = "models") -> None:
    autodiscover_models(package_name)
    await create_tables()


class ModelMeta(type):
    def __new__(mcls, name, bases, attrs):
        if name == "Model":
            return super().__new__(mcls, name, bases, attrs)

        fields = {}
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                value.name = key
                fields[key] = value
                attrs.pop(key)

        attrs["_fields"] = fields
        attrs["_table"] = name.lower()

        cls = super().__new__(mcls, name, bases, attrs)
        cls.objects = QuerySet(cls)
        register_model(cls)
        return cls


class Model(metaclass=ModelMeta):
    id = None

    def __init__(self, **kwargs):
        for field in self._fields:
            setattr(self, field, kwargs.get(field))

    @classmethod
    async def _create_table(cls):
        columns = []
        for field in cls._fields.values():
            columns.append(f"{field.name} {field.ddl()}")

        sql = f"""
        CREATE TABLE IF NOT EXISTS {cls._table} (
            {", ".join(columns)}
        )
        """
        await db.execute(sql)

    async def save(self):
        fields = list(self._fields.keys())
        values = []
        for name in fields:
            field = self._fields[name]
            value = getattr(self, name)
            if value is None and field.default is not None:
                value = field.default() if callable(field.default) else field.default
            values.append(value)
        values = tuple(values)
        placeholders = ", ".join("?" for _ in fields)

        sql = f"""
        INSERT INTO {self._table} ({", ".join(fields)})
        VALUES ({placeholders})
        """
        await db.execute(sql, values)
