import asyncio

import json
from typing import TYPE_CHECKING, Any

from openai import OpenAI

from agent.navigator.actions.structures import ActionProposal, ActionType

from agent.llm.prompt import SYSTEM_PROMPT
from agent.llm.tools import build_tool_specs

from models import ApiKey

if TYPE_CHECKING:
    from cli.config import RunConfig
    from agent.extractor.extractor import PageSnapshot


class OpenAIProposer:
    def __init__(self, config: 'RunConfig', timeout: int = 30):
        self.model = config.model
        self.client = OpenAI(
            api_key=asyncio.run(ApiKey.objects.get(name=config.provider)).value,
            timeout=timeout
        )

    def get_proposal(self, user_prompt: str, page_snapshot: 'PageSnapshot') -> 'ActionProposal':
        snapshot_payload = page_snapshot.to_payload()
        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": SYSTEM_PROMPT,
                        },
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": f"User goal: {user_prompt}",
                        },
                        {
                            "type": "input_text",
                            "text": f"Browser state: {json.dumps(snapshot_payload, ensure_ascii=True)}",
                        },
                    ],
                },
            ],
            tools=build_tool_specs(),
            tool_choice="required",
        )
        tool_call = self._extract_tool_call(response)
        return self._tool_call_to_proposal(tool_call)

    @staticmethod
    def _extract_tool_call(response: Any) -> dict[str, Any]:
        for item in getattr(response, "output", []):
            if isinstance(item, dict):
                item_type = item.get("type")
                if item_type in ("tool_call", "function_call"):
                    return {"name": item.get("name"), "arguments": item.get("arguments")}
                if item_type == "message":
                    for content in item.get("content", []):
                        if content.get("type") in ("tool_call", "function_call"):
                            return {
                                "name": content.get("name"),
                                "arguments": content.get("arguments"),
                            }
            if getattr(item, "type", None) in ("tool_call", "function_call"):
                return {
                    "name": getattr(item, "name", None),
                    "arguments": getattr(item, "arguments", None),
                }
            if getattr(item, "type", None) == "message":
                for content in getattr(item, "content", []) or []:
                    if getattr(content, "type", None) in ("tool_call", "function_call"):
                        return {
                            "name": getattr(content, "name", None),
                            "arguments": getattr(content, "arguments", None),
                        }
        raise ValueError("No tool call returned by the model.")

    @staticmethod
    def _tool_call_to_proposal(tool_call: dict[str, Any]) -> 'ActionProposal':
        name = tool_call.get("name")
        raw_args = tool_call.get("arguments", {}) or {}
        if isinstance(raw_args, str):
            try:
                raw_args = json.loads(raw_args)
            except json.JSONDecodeError:
                raw_args = {}

        action_type = ActionType(name)

        selector = raw_args.get("selector")
        value = raw_args.get("value") or raw_args.get("url")
        summary = raw_args.get("summary") or f"{action_type.value} {selector or value or ''}".strip()

        return ActionProposal(
            action_type=action_type,
            selector=selector,
            value=value,
            summary=summary,
        )
