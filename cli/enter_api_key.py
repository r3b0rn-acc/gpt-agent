import asyncio

from rich.text import Text

from cli import Console, STYLES

from typing import TYPE_CHECKING

from models import ApiKey

if TYPE_CHECKING:
    from cli.config import RunConfig


console = Console()


def enter_api_key(cfg: 'RunConfig') -> None:
    console.print(Text(f"No API key found for {cfg.provider.name}.", style=STYLES.warning))
    console.print(Text("Paste your key below; press Enter to continue.", style=STYLES.secondary))

    api_key = ''
    while not api_key:
        api_key = console.input(Text("API key: ", style=STYLES.primary)).strip()

        if not api_key:
            console.print(Text("API key cannot be empty. Try again.", style=STYLES.warning))

    asyncio.run(ApiKey(name=cfg.provider, value=api_key).save())
