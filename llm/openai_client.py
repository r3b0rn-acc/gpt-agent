from openai import OpenAI


class OpenAIClient:
    def __init__(self, api_key, model, timeout: float = 30):
        self.model = model
        self.client = OpenAI(api_key=api_key, timeout=timeout)
