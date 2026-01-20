from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from agent.navigator.actions.risk import assess_action_risk

if TYPE_CHECKING:
    from agent.extractor.extractor import PageSnapshot
    from agent.navigator.actions.structures import ActionType, ActionRisk, ActionProposal


@dataclass(frozen=True)
class Action:
    action_type: 'ActionType'
    selector: str | None
    value: str | None
    summary: str
    risk: 'ActionRisk'

    @staticmethod
    def with_assessed_risk(
        *,
        action_type: 'ActionType',
        selector: Optional[str],
        value: Optional[str],
        summary: str,
        snapshot: Optional['PageSnapshot'],
    ) -> 'Action':
        risk = assess_action_risk(
            action_type=action_type,
            selector=selector,
            value=value,
            snapshot=snapshot,
        )

        return Action(
            action_type=action_type,
            selector=selector,
            value=value,
            summary=summary,
            risk=risk,
        )

    @staticmethod
    def from_proposal(proposal: 'ActionProposal', snapshot: Optional['PageSnapshot']) -> 'Action':
        return Action.with_assessed_risk(
            action_type=proposal.action_type,
            selector=proposal.selector,
            value=proposal.value,
            summary=proposal.summary,
            snapshot=snapshot,
        )

    def __call__(self):
        ...
