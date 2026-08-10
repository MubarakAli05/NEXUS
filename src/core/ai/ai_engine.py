from src.core.ai.conversation import Conversation
from src.core.ai.model_manager import ModelManager

from src.core.memory.memory_manager import MemoryManager
from src.core.memory.memory_commands import MemoryCommand


class AIEngine:

    def __init__(self):

        self.conversation = Conversation()

        self.model = ModelManager()

        self.memory = MemoryManager()

    # ==========================================================
    # ASK STREAM
    # ==========================================================

    def ask_stream(self, message: str):

        message = message.strip()

        if not message:
            return

        # ======================================================
        # MEMORY COMMAND
        # ======================================================

        command = MemoryCommand.detect(
            message
        )

        if command:

            result = self._handle_memory_command(
                command
            )

            if result is not None:

                yield result

                return

        # ======================================================
        # NORMAL AI MESSAGE
        # ======================================================

        self.conversation.add_user_message(
            message
        )

        memory_context = (
            self._build_memory_context()
        )

        messages = (
            self.conversation.get_messages()
        )

        if memory_context:

            messages = [
                {
                    "role": "system",
                    "content": memory_context
                }
            ] + messages

        # ======================================================
        # STREAM FROM MODEL
        # ======================================================

        full_response = ""

        for chunk in self.model.generate_stream(
            messages
        ):

            full_response += chunk

            yield chunk

        # ======================================================
        # SAVE COMPLETE RESPONSE
        # ======================================================

        self.conversation.add_assistant_message(
            full_response
        )
    # ==========================================================
    # MEMORY COMMAND HANDLER
    # ==========================================================

    def _handle_memory_command(self, command):

        action = command.get(
            "action"
        )

        # ======================================================
        # REMEMBER
        # ======================================================

        if action == "remember":

            content = command.get(
                "content",
                ""
            )

            parsed = MemoryCommand.parse_memory(
                content
            )

            if not parsed:

                return (
                    "I couldn't understand "
                    "what you want me to remember."
                )

            category, key, value = parsed

            self.memory.remember(
                category,
                key,
                value
            )

            return (
                f"Got it. I'll remember that "
                f"{value}."
            )

        # ======================================================
        # LIST MEMORIES
        # ======================================================

        if action == "list":

            memories = (
                self.memory.get_all_memories()
            )

            if not memories:

                return (
                    "I don't have any stored "
                    "memories yet."
                )

            lines = [
                "Here's what I remember:"
            ]

            for memory in memories:

                (
                    _id,
                    category,
                    key,
                    value,
                    _created
                ) = memory

                lines.append(
                    f"• {key}: {value}"
                )

            return "\n".join(lines)

        # ======================================================
        # FORGET
        # ======================================================

        if action == "forget":

            content = command.get(
                "content",
                ""
            ).lower().strip()

            key = self._find_memory_key(
                content
            )

            if not key:

                return (
                    "I couldn't find a memory "
                    "matching that."
                )

            deleted = (
                self.memory.forget_by_key(
                    key
                )
            )

            if deleted:

                return (
                    f"Okay. I forgot "
                    f"{content}."
                )

            return (
                "I couldn't find that memory."
            )

        # ======================================================
        # CLEAR
        # ======================================================

        if action == "clear":

            self.memory.clear_all()

            return (
                "Done. I've cleared "
                "all stored memories."
            )

        return None

    # ==========================================================
    # FIND MEMORY KEY
    # ==========================================================

    def _find_memory_key(self, text):

        memories = (
            self.memory.get_all_memories()
        )

        text = text.lower()

        for memory in memories:

            (
                _id,
                _category,
                key,
                value,
                _created
            ) = memory

            key_lower = key.lower()

            value_lower = value.lower()

            if (
                text in key_lower
                or text in value_lower
                or key_lower in text
            ):

                return key

        return None

    # ==========================================================
    # MEMORY CONTEXT
    # ==========================================================

    def _build_memory_context(self):

        memories = (
            self.memory.get_all_memories()
        )

        if not memories:

            return ""

        lines = [
            "NEXUS MEMORY:",
            "Use these stored facts when relevant:",
            ""
        ]

        for memory in memories:

            (
                _id,
                category,
                key,
                value,
                _created
            ) = memory

            lines.append(
                f"{category}: {key} = {value}"
            )

        return "\n".join(lines)

    # ==========================================================
    # REMEMBER DIRECTLY
    # ==========================================================

    def remember(
        self,
        category: str,
        key: str,
        value: str
    ):

        return self.memory.remember(
            category,
            key,
            value
        )

    # ==========================================================
    # RECALL
    # ==========================================================

    def recall(self, key: str):

        return self.memory.recall(
            key
        )

    # ==========================================================
    # CLEAR CONVERSATION
    # ==========================================================

    def clear_conversation(self):

        self.conversation.clear()

    # ==========================================================
    # CLOSE
    # ==========================================================

    def close(self):

        self.memory.close()