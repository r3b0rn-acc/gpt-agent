from typing import TYPE_CHECKING, Optional

from agent.extractor.policy.base import apply_policy
from agent.extractor.structures import PageSnapshot, LinkInfo, InputInfo, ButtonInfo, ImageInfo

if TYPE_CHECKING:
    from playwright.async_api import Page
    from agent.extractor.policy.base import Policy


class Extractor:
    def __init__(self, page: 'Page', policies: Optional[list['Policy']] = None):
        self.page = page
        self.policies = policies or []

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

    @apply_policy("links")
    async def collect_links(self) -> list[LinkInfo]:
        await self.page.wait_for_load_state("networkidle")

        locator = self.page.locator("a")
        count = await locator.count()

        links = []

        for i in range(count):
            el = locator.nth(i)

            text = (await el.inner_text()).strip()
            href = await el.get_attribute("href") or ""
            selector = await self.build_selector_for_element(el)

            links.append(
                LinkInfo(
                    text=text,
                    href=href,
                    selector=selector,
                )
            )

        return links

    @apply_policy("inputs")
    async def collect_inputs(self) -> list[InputInfo]:
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

            inputs.append(
                InputInfo(
                    name=name,
                    input_type=input_type,
                    placeholder=placeholder,
                    selector=selector,
                )
            )

        return inputs

    @apply_policy("buttons")
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

    @apply_policy("images")
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
