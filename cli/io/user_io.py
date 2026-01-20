from rich.text import Text

from cli.io.console_singleton import Console
from cli.ui.styles import STYLES


console = Console()


class CLIUserIO:
    """
    Слой пользовательского ввода и вывода в CLI.

    Отвечает за:
    - отображение нейтральных сообщений агента (print);
    - получение пользовательского ввода (input).
    """
    @staticmethod
    def input():
        return console.input(Text(">> ", style=STYLES.secondary)).strip()

    @staticmethod
    def print(action_summary: str) -> None:
        console.print(Text.assemble(('• ', STYLES.secondary), (action_summary, STYLES.primary)))


class CLIClarificationIO:
    """
    Слой уточнений и подтверждений для потенциально значимых действий.

    Используется оркестратором в случаях, когда требуется:
    - запросить дополнительную информацию (ask);
    - подтвердить действие перед выполнением (confirm).
    """
    @staticmethod
    def ask(question: str) -> str:
        console.print(Text(question, style=STYLES.primary))
        return CLIUserIO().input()

    @staticmethod
    def confirm(action_summary: str) -> bool:
        console.print(Text(action_summary, style=STYLES.primary))
        answer = console.input(Text("Proceed? [y/N]: ", style=STYLES.warning)).strip().lower()
        return answer in ("y", "yes")
