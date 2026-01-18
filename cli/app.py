import asyncio

from pathlib import Path
from typing import Optional

import typer
from rich.text import Text

from cli import STYLES
from cli.config import Provider, Browser, RunConfig
from cli.console_singleton import Console
from cli.enter_api_key import enter_api_key
from cli.panel import show_main_panel
from cli.user_io import CLIUserIO
from models import ApiKey


app = typer.Typer(add_completion=False, no_args_is_help=True)
console = Console()


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
    cfg = RunConfig(
        provider=provider,
        model=model,
        browser=browser,
        profile_dir=profile,
        max_steps=max_steps,
        trace=trace,
    )
    try:
        show_main_panel(cfg)

        if not asyncio.run(ApiKey.objects.filter(name=provider).exists()):
            enter_api_key(cfg)

        while not task:
            task = CLIUserIO.input()
            if not task:
                console.print(Text("Task cannot be empty. Try again.", style=STYLES.warning))

        # asyncio.run(...)
        pass
    except KeyboardInterrupt:
        console.print('\nInterrupted by user.')
