from rich.console import Console as RichConsole


class Console(RichConsole):
    """
    Синглтон консоли.

    В документации рекомендуется иметь 1 инстанс консоли (для большинства случаев)
    https://rich.readthedocs.io/en/latest/console.html#:~:text=Most%20applications%20will%20require%20a%20single%20Console%20instance
    """
    _instance: "Console | None" = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs):
        if getattr(self, "_initialized", False):
            return

        super().__init__(*args, **kwargs)
        self._initialized = True
