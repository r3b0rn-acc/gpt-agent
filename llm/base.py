from typing import Protocol


class LLMClient(Protocol):
    def __init__(self, api_key, model):
        ...
