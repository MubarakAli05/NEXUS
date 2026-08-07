import ollama

from src.core.ai.prompt_manager import SYSTEM_PROMPT


class ModelManager:

    def __init__(self, model="qwen3:4b"):
        self.model = model

    def generate(self, messages):

        chat = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        chat.extend(messages)

        response = ollama.chat(
            model=self.model,
            messages=chat
        )

        return response["message"]["content"]