from typing import Optional

from rich.text import Text

from cli.io import Console, CLIUserIO
from cli.ui.styles import STYLES


console = Console()


def get_task() -> Optional[str]:
    """Сценарий получения задачи для агента от пользователя"""

    while True:
        try:
            task = CLIUserIO.input()
        except (EOFError, KeyboardInterrupt):
            return None

        task = task.strip() if task else None
        if not task:
            console.print(Text('Task cannot be empty. Try again.', style=STYLES.warning))
            continue

        return task
