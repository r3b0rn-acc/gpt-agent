from dataclasses import dataclass
from enum import Enum
from typing import Any


class ActionType(str, Enum):
    open = "open"
    click = "click"
    type = "type"
    press = "press"
    wait = "wait"
    back = "back"
    forward = "forward"
    reload = "reload"
    scroll = "scroll"
    snapshot = "snapshot"
    done = "done"


class ActionRisk(str, Enum):
    safe = "safe"
    confirm = "confirm"
    destructive = "destructive"


@dataclass(frozen=True)
class ActionSpec:
    name: 'ActionType'
    description: str
    parameters: dict[str, Any]


@dataclass(frozen=True)
class ActionProposal:
    action_type: 'ActionType'
    selector: str | None
    value: str | None
    summary: str
