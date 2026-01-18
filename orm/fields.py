from abc import ABC, abstractmethod


class BaseField(ABC):
    sql_type: str
    name: str | None

    def __init__(self) -> None:
        self.name = None

    def ddl(self) -> str:
        parts = [self.sql_type, *self._ddl_constraints()]
        return " ".join(parts)

    @abstractmethod
    def _ddl_constraints(self) -> list[str]:
        raise NotImplementedError


class Field(BaseField):
    def __init__(self, primary_key=False, null=False, default=None):
        super().__init__()
        self.primary_key = primary_key
        self.null = null
        self.default = default

    def _render_default(self) -> str:
        value = self.default() if callable(self.default) else self.default
        if isinstance(value, str):
            escaped = value.replace("'", "''")
            return f"'{escaped}'"
        if isinstance(value, bool):
            return "1" if value else "0"
        if value is None:
            return "NULL"
        return str(value)

    def _ddl_constraints(self) -> list[str]:
        parts = []
        if self.primary_key:
            parts.append("PRIMARY KEY")
        if not self.null:
            parts.append("NOT NULL")
        if self.default is not None:
            parts.append(f"DEFAULT {self._render_default()}")
        return parts


class IntegerField(Field):
    sql_type = "INTEGER"

    def _ddl_constraints(self) -> list[str]:
        if self.primary_key:
            return ["PRIMARY KEY AUTOINCREMENT"]
        return super()._ddl_constraints()


class TextField(Field):
    sql_type = "TEXT"
