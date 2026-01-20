import tomllib
from pathlib import Path
from typing import TYPE_CHECKING

from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from cli.io import Console
from cli.ui.styles import STYLES

if TYPE_CHECKING:
    from cli.app import RunConfig


console = Console()


def _get_version() -> str:
    pyproject_path = Path("pyproject.toml")

    with pyproject_path.open("rb") as f:
        data = tomllib.load(f)
        return data['project']['version']


def show_main_panel(cfg: 'RunConfig') -> None:
    """Отображает панель с основной информацией по агенту"""

    header = Table.grid(expand=True)

    header.add_column(justify="left", no_wrap=True)
    header.add_column(justify="right", no_wrap=True)
    header.add_row(
        Text.assemble((">_ ", STYLES.secondary), ("gpt-agent", "bold white"),),
        Text(f"(v{_get_version()})", style=STYLES.secondary),
    )

    table = Table.grid(expand=True)

    table.add_column(justify="left", no_wrap=True)
    table.add_column(justify="right")
    table.add_row(
        Text("provider:", style=STYLES.secondary),
        Text(cfg.provider, style=STYLES.primary)
    )
    table.add_row(
        Text("model:", style=STYLES.secondary),
        Text(cfg.model, style=STYLES.primary)
    )
    table.add_row(
        Text("browser:", style=STYLES.secondary),
        Text(cfg.browser, style=STYLES.primary)
    )

    console.print(Panel(Group(header, Text(""), table), width=40))
