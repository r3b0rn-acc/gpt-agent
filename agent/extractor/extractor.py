from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.async_api import Page


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

    def to_payload(
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


class Extractor:
    def __init__(self, page: 'Page'):
        self.page = page

    async def extract(self) -> PageSnapshot:
        return PageSnapshot(
            url=self.page.url,
            title=await self.page.title(),
            text=await self.page.inner_text("body"),
            links=await self.collect_links(),
            inputs=await self.collect_inputs(),
            buttons=await self.collect_buttons(),
            images=await self.collect_images(),
        )

    @staticmethod
    async def build_selector_for_element(el):
        return await el.evaluate("""
        node => {
            if (node.id)
                return `#${node.id}`;

            const aria = node.getAttribute('aria-label');
            if (aria)
                return `[aria-label="${aria}"]`;

            if (node.name)
                return `${node.tagName.toLowerCase()}[name="${node.name}"]`;

            if (node.placeholder)
                return `${node.tagName.toLowerCase()}[placeholder="${node.placeholder}"]`;

            if (node.className) {
                const cls = node.className.split(' ')
                    .filter(c => !c.startsWith('css-'))
                    .slice(0, 2)
                    .join('.');
                if (cls)
                    return `${node.tagName.toLowerCase()}.${cls}`;
            }

            return node.tagName.toLowerCase();
        }
        """)

    async def collect_links(self) -> list[LinkInfo]:
        await self.page.wait_for_load_state("networkidle")

        locator = self.page.locator("a[href]")
        count = await locator.count()

        links = []

        for i in range(count):
            el = locator.nth(i)

            text = (await el.inner_text()).strip()
            href = await el.get_attribute("href")
            selector = await self.build_selector_for_element(el)

            if not href:
                continue

            links.append(
                LinkInfo(
                    text=text,
                    href=href,
                    selector=selector,
                )
            )

        return links

    async def collect_inputs(self, include_hidden=False) -> list[InputInfo]:
        await self.page.wait_for_load_state("networkidle")

        locator = self.page.locator("input")
        count = await locator.count()

        inputs = []

        for i in range(count):
            el = locator.nth(i)

            name = await el.get_attribute("name") or ""
            input_type = await el.get_attribute("type") or "text"
            placeholder = await el.get_attribute("placeholder") or ""
            selector = await self.build_selector_for_element(el)

            if not include_hidden and input_type == "hidden":
                continue

            inputs.append(
                InputInfo(
                    name=name,
                    input_type=input_type,
                    placeholder=placeholder,
                    selector=selector,
                )
            )

        return inputs

    async def collect_buttons(self) -> list[ButtonInfo]:
        await self.page.wait_for_load_state("networkidle")

        locator = self.page.locator("button")
        count = await locator.count()

        buttons = []

        for i in range(count):
            el = locator.nth(i)

            text = (await el.inner_text()).strip()
            selector = await self.build_selector_for_element(el)
            aria_label = await el.get_attribute("aria-label") or ""
            button_type = await el.get_attribute("type") or ""
            disabled = await el.get_attribute("disabled") or False

            buttons.append(
                ButtonInfo(
                    text=text,
                    selector=selector,
                    aria_label=aria_label,
                    button_type=button_type,
                    disabled=disabled,
                )
            )

        return buttons

    async def collect_images(self) -> list[ImageInfo]:
        await self.page.wait_for_load_state("networkidle")

        locator = self.page.locator("img")
        count = await locator.count()

        images = []

        for i in range(count):
            el = locator.nth(i)

            src = await el.get_attribute("src") or ""
            alt = await el.get_attribute("alt") or ""
            selector = await self.build_selector_for_element(el)
            title = await el.get_attribute("title") or ""
            aria_label = await el.get_attribute("aria-label") or ""
            width = await el.get_attribute("width") or 0
            height = await el.get_attribute("height") or 0

            images.append(
                ImageInfo(
                    src=src,
                    alt=alt,
                    selector=selector,
                    title=title,
                    aria_label=aria_label,
                    width=width,
                    height=height,
                )
            )

        return images
