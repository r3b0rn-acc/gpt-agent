from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class LinkInfo:
    text: str
    href: str
    selector: str = ""


@dataclass(frozen=True)
class InputInfo:
    name: str
    input_type: str
    placeholder: str
    selector: str = ""


@dataclass(frozen=True)
class ButtonInfo:
    text: str
    selector: str
    aria_label: str = ""
    button_type: str = ""
    disabled: bool = False


@dataclass(frozen=True)
class ImageInfo:
    src: str
    alt: str
    selector: str
    title: str = ""
    aria_label: str = ""
    width: int = 0
    height: int = 0
    is_icon: bool = False


@dataclass(frozen=True)
class PageSnapshot:
    url: str
    title: str
    text: str
    links: List[LinkInfo]
    inputs: List[InputInfo]
    buttons: List[ButtonInfo]
    images: List[ImageInfo]
    screenshot_base64: Optional[str] = None

    def to_summary(self, max_len: int = 800) -> str:
        text = self.text
        if len(text) > max_len:
            text = text[: max_len - 3] + "..."
        return text

    def to_llm_payload(
        self,
        *,
        max_text_len: int = 2000,
        max_items: int = 50,
        include_screenshot: bool = False,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "url": self.url,
            "title": self.title,
            "text": self.to_summary(max_text_len),
            "links": [asdict(link) for link in self.links[:max_items]],
            "inputs": [asdict(input_info) for input_info in self.inputs[:max_items]],
            "buttons": [asdict(button) for button in self.buttons[:max_items]],
            "images": [asdict(image) for image in self.images[:max_items]],
        }
        if include_screenshot and self.screenshot_base64:
            payload["screenshot_base64"] = self.screenshot_base64

        return payload
