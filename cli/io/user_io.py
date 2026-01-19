from rich.text import Text

from cli.io.console_singleton import Console
from cli.ui.styles import STYLES


console = Console()


class CLIUserIO:
    """
    Слой через который LLM будет общаться с юзером.
    Оркестратор должен вызывать ask() / confirm().
    """

    @staticmethod
    def input():
        return console.input(Text(">> ", style=STYLES.secondary)).strip()

    def ask(self, question: str) -> str:
        console.print(Text(question, style=STYLES.primary))
        return self.input()

    @staticmethod
    def confirm(action_summary: str) -> bool:
        console.print(Text(action_summary, style=STYLES.primary))
        answer = console.input(Text("Proceed? [y/N]: ", style=STYLES.warning)).strip().lower()
        return answer in ("y", "yes")
