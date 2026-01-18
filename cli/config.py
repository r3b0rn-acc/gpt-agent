from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class Provider(str, Enum):
    openai = 'openai'
    anthropic = 'anthropic'


class Browser(str, Enum):
    chrome = 'chrome'
    firefox = 'firefox'


class RunConfig(BaseModel):
    provider: Provider
    model: str
    browser: Browser
    profile_dir: Path
    max_steps: int = Field(..., gt=0)
    trace: bool

    @field_validator('model', mode='before')
    @classmethod
    def model_non_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError('model must be a non-empty string')
        return value
