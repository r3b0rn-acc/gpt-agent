from typing import Iterable, Any

from agent.navigator.actions.structures import ActionType, ActionSpec


_ACTION_SPECS: dict[ActionType, ActionSpec] = {
    ActionType.open: ActionSpec(
        name=ActionType.open,
        description="Open URL on current browser page",
        parameters={
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                },
            },
            "required": ["url"],
        },
    ),
    ActionType.click: ActionSpec(
        name=ActionType.click,
        description="Click on page element",
        parameters={
            "type": "object",
            "properties": {
                "selector": {
                    "type": "string",
                    "description": "CSS or XPath selector",
                },
            },
            "required": ["selector"],
        },
    ),
    ActionType.type: ActionSpec(
        name=ActionType.type,
        description="Type text in input element",
        parameters={
            "type": "object",
            "properties": {
                "selector": {
                    "type": "string",
                },
                "value": {
                    "type": "string",
                },
            },
            "required": ["selector", "value"],
        },
    ),
    ActionType.press: ActionSpec(
        name=ActionType.press,
        description="Press button or keyboard shortcut",
        parameters={
            "type": "object",
            "properties": {
                "value": {
                    "type": "string",
                    "description": "For example: Enter, Escape, Ctrl+L",
                },
            },
            "required": ["value"],
        },
    ),
    ActionType.wait: ActionSpec(
        name=ActionType.wait,
        description="Wait for the specified number of milliseconds",
        parameters={
            "type": "object",
            "properties": {
                "value": {
                    "type": "integer",
                    "description": "Wait time in milliseconds",
                    "minimum": 0,
                },
            },
            "required": ["value"],
        },
    ),
    ActionType.scroll: ActionSpec(
        name=ActionType.scroll,
        description="Scroll the page",
        parameters={
            "type": "object",
            "properties": {
                "value": {
                    "type": "string",
                    "description": "up | down | top | bottom",
                }
            },
            "required": ["value"],
        },
    ),
    ActionType.back: ActionSpec(
        name=ActionType.back,
        description="Return to the previous page",
        parameters={
            "type": "object",
            "properties": {},
        },
    ),
    ActionType.forward: ActionSpec(
        name=ActionType.forward,
        description="Skip forward in history",
        parameters={
            "type": "object",
            "properties": {},
        },
    ),
    ActionType.reload: ActionSpec(
        name=ActionType.reload,
        description="Reload the page",
        parameters={
            "type": "object",
            "properties": {},
        },
    ),
    ActionType.snapshot: ActionSpec(
        name=ActionType.snapshot,
        description="Request page snapshot if a new page state is implied",
        parameters={
            "type": "object",
            "properties": {},
        },
    ),
    ActionType.done: ActionSpec(
        name=ActionType.done,
        description="Notify that the task is fully completed",
        parameters={
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "Brief summary of actions taken",
                },
            },
            "required": ["summary"],
        },
    ),
}


def iter_action_specs() -> Iterable[ActionSpec]:
    return _ACTION_SPECS.values()


def make_tool_spec(name: str, description: str, parameters: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": "function",
        "name": name,
        "description": description,
        "parameters": parameters,
    }


def build_tool_specs() -> list[dict[str, Any]]:
    return [
        make_tool_spec(
            name=spec.name.value,
            description=spec.description,
            parameters=spec.parameters,
        )
        for spec in iter_action_specs()
    ]
