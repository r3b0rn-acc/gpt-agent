from dataclasses import dataclass
from enum import Enum

from pathlib import Path

import typer
from rich.console import Console


app = typer.Typer(add_completion=False, no_args_is_help=True)
console = Console()


class Provider(str, Enum):
    openai = 'openai'
    anthropic = 'anthropic'


@dataclass
class RunConfig:
    provider: Provider
    model: str
    profile_dir: Path
    max_steps: int
    trace: bool

