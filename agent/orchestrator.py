from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cli.config import RunConfig


class Orchestrator:
    def __init__(self, cfg: 'RunConfig'):
        self.cfg = cfg

    async def run(self, task: str):
        if not task or not task.strip():
            raise ValueError('Task cannot be empty.')

