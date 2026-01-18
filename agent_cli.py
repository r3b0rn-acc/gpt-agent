import asyncio

from cli.app import app
from orm.model import init_models


if __name__ == "__main__":
    asyncio.run(init_models())
    app()
