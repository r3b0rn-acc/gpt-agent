import asyncio
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional

import typer
from dotenv import load_dotenv

from cli.console_singleton import Console


app = typer.Typer(add_completion=False, no_args_is_help=True)
console = Console()


class Provider(str, Enum):
    openai = 'openai'
    anthropic = 'anthropic'


class Browser(str, Enum):
    chrome = 'chrome'
    firefox = 'firefox'


@dataclass
class RunConfig:
    provider: Provider
    model: str
    browser: Browser
    profile_dir: Path
    max_steps: int
    trace: bool


@app.command()
def run(
    task: Optional[str] = typer.Argument(None, help='Task for the agent'),
    provider: Provider = typer.Option(Provider.openai, '--provider', '-p'),
    model: str = typer.Option('gpt-4.1', '--model', '-m'),
    browser: Browser = typer.Option(Browser.chrome, '--browser', '-b'),
    profile: Path = typer.Option(Path('profiles/user1'), '--profile'),
    max_steps: int = typer.Option(80, '--max-steps'),
    trace: bool = typer.Option(False, '--trace', help='Enable Playwright tracing (if implemented)'),
):
    """
    Runs agent
    """
    load_dotenv()

    cfg = RunConfig(
        provider=provider,
        model=model,
        browser=browser,
        profile_dir=profile,
        max_steps=max_steps,
        trace=trace,
    )

    try:
        asyncio.run(...)
    except KeyboardInterrupt:
        console.print('\nInterrupted by user.')
