from typing import TYPE_CHECKING, Optional, Protocol, Any

from agent.navigator.actions import Action
from agent.navigator.actions.structures import ActionRisk
from cli.config import Provider

from agent.llm.anthropic_proposer import ClaudeProposer
from agent.llm.openai_proposer import OpenAIProposer

if TYPE_CHECKING:
    from agent.llm.base import Proposer
    from cli.config import RunConfig
    from agent.extractor.extractor import PageSnapshot
    from agent.navigator.actions.structures import ActionProposal


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
    """
    Основной координатор выполнения задач агента.

    Orchestrator:
    - связывает LLM proposer, браузерное состояние и навигатор;
    - управляет жизненным циклом пользовательской задачи;

    Является точкой композиции всех слоёв системы.
    """
    def __init__(
            self,
            config: 'RunConfig',
            io_manager: Optional['IOManager'] = None,
            clarification_manager: Optional['ClarificationManager'] = None
    ) -> None:

        self.cfg = config
        self.io_manager = io_manager
        self.clarification_manager = clarification_manager

        self.llm_proposer = self._build_llm_proposer()

    async def run(self, task: str) -> None:
        """
        Основная корутина.

        Запускает в работу агента, информирует и опрашивает пользователя о действиях агента
        при наличии io_manager и clarification_manager.
        """
        if not task or not task.strip():
            raise ValueError('Task cannot be empty.')

        page_snapshot = await self._get_page_snapshot(task)

        proposal = self.llm_proposer.get_proposal(task, page_snapshot)
        action = self._build_action(proposal, page_snapshot)

        if self.clarification_manager and self._requires_confirmation(action):
            if not self.clarification_manager.confirm(action.summary):
                return

        elif self.io_manager:
            self.io_manager.print(action.summary)

        await self._invoke_action(action)

    def _build_llm_proposer(self) -> 'Proposer':
        match self.cfg.provider:
            case Provider.openai:
                return OpenAIProposer(self.cfg)
            case Provider.anthropic:
                return ClaudeProposer(self.cfg)

    @staticmethod
    def _build_action(proposal: 'ActionProposal', page_snapshot: 'PageSnapshot') -> Action:
        """Преобразует предложение действия в исполняемое действие агента"""

        return Action.from_proposal(proposal, page_snapshot)

    @staticmethod
    def _requires_confirmation(action: Action) -> bool:
        """Определяет, требует ли действие подтверждения пользователя"""

        return action.risk in {ActionRisk.confirm, ActionRisk.destructive}

    async def _get_page_snapshot(self, task: str) -> 'PageSnapshot':
        """Получает актуальный снапшот страницы перед принятием решения"""

    async def _invoke_action(self, action: Action) -> None:
        """Выполняет действие агента"""
