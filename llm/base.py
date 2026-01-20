from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from cli.config import RunConfig
    from agent.extractor.extractor import PageSnapshot
    from agent.navigator.actions.structures import ActionProposal


class Proposer(Protocol):
    """
    Протокол компонента, отвечающего за генерацию следующего действия агента.

    Proposer:
    - инкапсулирует взаимодействие с LLM;
    - анализирует пользовательский запрос и текущее состояние страницы;
    - формирует структурированное предложение действия (ActionProposal).

    Не выполняет действий самостоятельно.
    """
    def __init__(self, config: 'RunConfig', timeout: int):
        pass

    def get_proposal(self, user_prompt: str, page_snapshot: 'PageSnapshot') -> 'ActionProposal':
        """
        Формирует предложение следующего действия агента.

        Возвращает ActionProposal без побочных эффектов, на основании запроса пользователя и снапшота страницы.
        """
