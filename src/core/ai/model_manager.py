import ollama

from src.core.ai.prompt_manager import SYSTEM_PROMPT


class ModelManager:

    def __init__(self, model="qwen3:4b-instruct"):

        self.model = model

    # ==========================================================
    # NORMAL GENERATION
    # ==========================================================

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

    # ==========================================================
    # STREAMING GENERATION
    # ==========================================================

    def generate_stream(self, messages):

        chat = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        chat.extend(messages)

        stream = ollama.chat(
            model=self.model,
            messages=chat,
            stream=True
        )

        for chunk in stream:

            content = chunk["message"]["content"]

            if content:

                yield content