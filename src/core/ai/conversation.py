class Conversation:

    def __init__(self, max_messages=20):

        self.messages = []

        self.max_messages = max_messages

    # ==========================================================
    # ADD USER MESSAGE
    # ==========================================================

    def add_user_message(self, message: str):

        if not message:
            return

        self.messages.append({
            "role": "user",
            "content": message
        })

        self._trim_history()

    # ==========================================================
    # ADD ASSISTANT MESSAGE
    # ==========================================================

    def add_assistant_message(self, message: str):

        if not message:
            return

        self.messages.append({
            "role": "assistant",
            "content": message
        })

        self._trim_history()

    # ==========================================================
    # GET MESSAGES
    # ==========================================================

    def get_messages(self):

        return self.messages.copy()

    # ==========================================================
    # GET LAST MESSAGES
    # ==========================================================

    def get_recent_messages(self, count=10):

        return self.messages[-count:]

    # ==========================================================
    # TRIM HISTORY
    # ==========================================================

    def _trim_history(self):

        if len(self.messages) > self.max_messages:

            self.messages = self.messages[
                -self.max_messages:
            ]

    # ==========================================================
    # CLEAR
    # ==========================================================

    def clear(self):

        self.messages.clear()

    # ==========================================================
    # MESSAGE COUNT
    # ==========================================================

    def count(self):

        return len(self.messages)

    # ==========================================================
    # LAST MESSAGE
    # ==========================================================

    def last_message(self):

        if not self.messages:
            return None

        return self.messages[-1]