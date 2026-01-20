from typing import TYPE_CHECKING, Optional

from agent.navigator.actions.structures import ActionType, ActionRisk

if TYPE_CHECKING:
    from agent.extractor.structures import PageSnapshot


_DESTRUCTIVE_KEYWORDS = (
    "delete",
    "remove",
    "erase",
    "destroy",
    "wipe",
    "clear",
    "reset",
    "revoke",
    "unsubscribe",
    "cancel subscription",
    "permanently",
)

_CONFIRM_KEYWORDS = (
    "submit",
    "send",
    "save",
    "confirm",
    "approve",
    "accept",
    "apply",
    "publish",
    "post",
    "checkout",
    "purchase",
    "pay",
    "buy",
    "register",
    "sign up",
    "sign in",
    "log in",
    "logout",
    "sign out",
    "update",
    "change",
    "join",
)

_SAFE_KEYWORDS = (
    "search",
    "view",
    "learn more",
    "details"
)


def _normalize(text: str) -> str:
    return " ".join(text.lower().split())


def _element_context(snapshot: 'PageSnapshot', selector: str) -> str:
    for button in snapshot.buttons:
        if button.selector == selector:
            parts = [button.text, button.aria_label, button.button_type]
            return _normalize(" ".join(p for p in parts if p))

    for link in snapshot.links:
        if link.selector == selector:
            parts = [link.text, link.href]
            return _normalize(" ".join(p for p in parts if p))

    for input_info in snapshot.inputs:
        if input_info.selector == selector:
            parts = [input_info.name, input_info.placeholder, input_info.input_type]
            return _normalize(" ".join(p for p in parts if p))

    return ""


def _contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    return any(keyword in text for keyword in keywords)


def assess_action_risk(
    *,
    action_type: 'ActionType',
    selector: Optional[str],
    value: Optional[str],
    snapshot: Optional['PageSnapshot'],
) -> 'ActionRisk':
    if action_type in {
        ActionType.open,
        ActionType.wait,
        ActionType.back,
        ActionType.forward,
        ActionType.reload,
        ActionType.scroll,
        ActionType.snapshot,
        ActionType.done,
    }:
        return ActionRisk.safe

    context = ""
    if snapshot and selector:
        context = _element_context(snapshot, selector)

    if context:
        if _contains_any(context, _DESTRUCTIVE_KEYWORDS):
            return ActionRisk.destructive
        if _contains_any(context, _CONFIRM_KEYWORDS):
            return ActionRisk.confirm
        if _contains_any(context, _SAFE_KEYWORDS):
            return ActionRisk.safe

    if action_type == ActionType.type:
        if snapshot and selector:
            for input_info in snapshot.inputs:
                if input_info.selector == selector:
                    input_type = _normalize(input_info.input_type)
                    name = _normalize(input_info.name)
                    placeholder = _normalize(input_info.placeholder)
                    if "search" in name or "search" in placeholder or input_type == "search":
                        return ActionRisk.safe
                    if input_type == "password":
                        return ActionRisk.confirm
                    if any(keyword in name for keyword in ("card", "credit", "cvv", "ssn", "iban")):
                        return ActionRisk.confirm
                    break
        return ActionRisk.confirm

    if action_type in {ActionType.click, ActionType.press}:
        if value and _contains_any(_normalize(value), _DESTRUCTIVE_KEYWORDS):
            return ActionRisk.destructive
        return ActionRisk.confirm

    return ActionRisk.confirm
