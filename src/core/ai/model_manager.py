import ollama

from src.core.ai.prompt_manager import SYSTEM_PROMPT


class ModelManager:

    def __init__(self, model="qwen3:4b-instruct"):
        self.model = model

    # ==========================================================
    # BUILD CHAT
    # ==========================================================

    def build_chat(self, messages):

        chat = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        chat.extend(messages)

        return chat

    # ==========================================================
    # NORMAL RESPONSE
    # ==========================================================

    def generate(self, messages):

        chat = self.build_chat(messages)

        response = ollama.chat(
            model=self.model,
            messages=chat,
            think=False,
        )

        # Current Ollama versions expose the final answer
        # separately from the reasoning when available.
        content = response.message.content or ""

        return self.clean_response(content)

    # ==========================================================
    # STREAMING RESPONSE
    # ==========================================================

    def generate_stream(self, messages):

        chat = self.build_chat(messages)

        stream = ollama.chat(
            model=self.model,
            messages=chat,
            stream=True,
            think=False,
        )

        for chunk in stream:

            # ----------------------------------------------
            # IMPORTANT:
            #
            # If Ollama gives us a separate thinking field,
            # IGNORE IT completely.
            # ----------------------------------------------

            thinking = getattr(
                chunk.message,
                "thinking",
                None
            )

            if thinking:
                continue

            # ----------------------------------------------
            # Only send actual answer content to UI.
            # ----------------------------------------------

            content = getattr(
                chunk.message,
                "content",
                ""
            )

            if not content:
                continue

            yield content

    # ==========================================================
    # CLEAN RESPONSE
    # ==========================================================

    def clean_response(self, text):

        if not text:
            return ""

        # Remove explicit thinking blocks if they somehow
        # still appear in content.

        while "<think>" in text and "</think>" in text:

            before, after = text.split(
                "<think>",
                1
            )

            _, after = after.split(
                "</think>",
                1
            )

            text = before + after

        # Handle a dangling closing tag.

        if "</think>" in text:

            text = text.split(
                "</think>",
                1
            )[1]

        text = text.replace(
            "<think>",
            ""
        )

        text = text.replace(
            "</think>",
            ""
        )

        return text.strip()