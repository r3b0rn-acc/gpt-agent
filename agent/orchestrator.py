from typing import TYPE_CHECKING, Optional, Protocol, Any

from agent.navigator import Action
from agent.risk import ActionRisk
from cli.config import Provider

from llm.anthropic_proposer import ClaudeProposer
from llm.openai_proposer import OpenAIProposer

if TYPE_CHECKING:
    from llm.base import Proposer
    from cli.config import RunConfig
    from agent.navigator import ActionProposal
    from agent.extractor.extractor import PageSnapshot


class IOManager(Protocol):
    """
    Протокол слоя пользовательского вывода.

    Используется оркестратором для отображения информации о действиях агента.
    """
    @staticmethod
    def print(text: Any) -> None:
        """Отображает объекты в строковом представлении"""


class ClarificationManager(Protocol):
    """
    Протокол слоя уточнений и подтверждений.

    Применяется для потенциально рискованных или необратимых действий агента.
    """
    @staticmethod
    def confirm(text: str) -> bool:
        """Запрашивает подтверждение действия у пользователя"""

    @staticmethod
    def ask(text: str) -> str:
        """Запрашивает дополнительную информацию по задаче или действию"""


class Orchestrator:
    def __init__(self, cfg: 'RunConfig'):
        self.cfg = cfg

    async def run(self, task: str):
        if not task or not task.strip():
            raise ValueError('Task cannot be empty.')

