from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cli.config import RunConfig
    from agent.navigator import ActionProposal
    from agent.extractor.extractor import PageSnapshot


class ClaudeProposer:
    def __init__(self, config: 'RunConfig', timeout: int = 30):
        ...

    def get_proposal(self, user_prompt: str, page_snapshot: 'PageSnapshot') -> 'ActionProposal':
        ...