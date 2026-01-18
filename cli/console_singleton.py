from rich.console import Console as RichConsole


class Console(RichConsole):
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
