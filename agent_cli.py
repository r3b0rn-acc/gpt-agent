import asyncio

from cli.app import app
from orm.model import init_models


"""
Точка входа в CLI-приложение.

Отвечает за:
- инициализацию ORM-моделей;
- запуск CLI, построенного на Typer.
"""


if __name__ == "__main__":
    asyncio.run(init_models())
    app()
