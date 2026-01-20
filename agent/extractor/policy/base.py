from functools import wraps
from typing import Iterable, Literal, Callable, Awaitable, Any


PolicyTarget = Literal["links", "inputs", "buttons", "images"]
PolicyItems = Iterable["LinkInfo"] | Iterable["InputInfo"] | Iterable["ButtonInfo"] | Iterable["ImageInfo"]


def apply_policy(
        target: PolicyTarget,
) -> Callable[[Callable[..., Awaitable[list[Any]]]], Callable[..., Awaitable[list[Any]]]]:
    """Декоратор для сборщиков DOM объектов класса Extractor"""
    def decorator(
            func: Callable[..., Awaitable[list[Any]]],
    ) -> Callable[..., Awaitable[list[Any]]]:
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            items = await func(self, *args, **kwargs)
            for policy in self.policies:
                items = list(policy.apply(target, items))

            return items

        return wrapper

    return decorator


class Policy:
    """Базовый класс политики Extractor сборщиков"""
    def apply(
            self,
            target: PolicyTarget,
            items: PolicyItems,
    ) -> PolicyItems:
        return items
