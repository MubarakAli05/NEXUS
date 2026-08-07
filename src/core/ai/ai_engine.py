from src.core.ai.conversation import Conversation
from src.core.ai.model_manager import ModelManager


class AIEngine:

    def __init__(self):

        self.conversation = Conversation()

        self.model = ModelManager()

    def ask(self, message: str):

        self.conversation.add_user_message(message)

        reply = self.model.generate(
            self.conversation.get_messages()
        )

        self.conversation.add_assistant_message(reply)

        return reply

    def clear_conversation(self):

        self.conversation.clear()