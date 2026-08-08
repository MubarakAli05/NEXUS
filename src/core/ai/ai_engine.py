from src.core.ai.conversation import Conversation
from src.core.ai.model_manager import ModelManager


class AIEngine:

    def __init__(self):

        self.conversation = Conversation()

        self.model = ModelManager()

    # ==========================================================
    # NORMAL RESPONSE
    # ==========================================================

    def ask(self, message: str):

        self.conversation.add_user_message(message)

        reply = self.model.generate(
            self.conversation.get_messages()
        )

        self.conversation.add_assistant_message(reply)

        return reply

    # ==========================================================
    # STREAMING RESPONSE
    # ==========================================================

    def ask_stream(self, message: str):

        self.conversation.add_user_message(message)

        full_response = ""

        for chunk in self.model.generate_stream(
            self.conversation.get_messages()
        ):

            full_response += chunk

            yield chunk

        # Store the COMPLETE response only after
        # streaming has finished.

        self.conversation.add_assistant_message(
            full_response
        )

    # ==========================================================
    # CLEAR CONVERSATION
    # ==========================================================

    def clear_conversation(self):

        self.conversation.clear()