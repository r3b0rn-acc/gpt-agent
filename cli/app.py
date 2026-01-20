import typer

import asyncio

from pathlib import Path
from typing import Optional

from rich.text import Text

from agent.orchestrator import Orchestrator

from cli.config import Provider, Browser, RunConfig
from cli.io import Console, CLIUserIO, CLIClarificationIO
from cli.ui.enter_api_key import enter_api_key
from cli.ui.get_task import get_task
from cli.ui.panel import show_main_panel
from cli.ui.styles import STYLES

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
    Runs browser surfing agent
    """
    cfg = RunConfig(
        provider=provider,
        model=model,
        browser=browser,
        profile_dir=profile,
        max_steps=max_steps,
        trace=trace,
    )

    orchestrator = Orchestrator(
        config=cfg,
        io_manager=CLIUserIO(),
        clarification_manager=CLIClarificationIO(),
    )

    async def run_cli():
        show_main_panel(cfg)

        if not await ApiKey.objects.filter(name=cfg.provider).exists():
            enter_api_key(cfg)

        current_task = task
        if current_task:
            console.print(Text.assemble((">> ", STYLES.secondary), (current_task, STYLES.primary)))

        while True:
            current_task = current_task or get_task()
            if not current_task:
                break
            await orchestrator.run(current_task)
            current_task = None

    try:
        asyncio.run(run_cli())
    except KeyboardInterrupt:
        console.print('\nInterrupted by user.')
