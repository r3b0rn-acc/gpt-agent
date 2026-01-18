from dataclasses import dataclass
from enum import Enum


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


@dataclass(frozen=True)
class Action:
    action_type: ActionType
