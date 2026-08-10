from src.core.voice.speech_to_text import SpeechToText
from src.core.voice.text_to_speech import TextToSpeech

from src.core.intent.intent_engine import IntentEngine
from src.core.intent.intents import IntentType

from src.core.actions.action_engine import ActionEngine


class VoiceAssistant:

    def __init__(self, ai):

        self.ai = ai

        # ======================================================
        # VOICE
        # ======================================================

        self.stt = SpeechToText()
        self.tts = TextToSpeech()

        # ======================================================
        # UNDERSTANDING
        # ======================================================

        self.intent_engine = IntentEngine()

        # ======================================================
        # COMPUTER ACTIONS
        # ======================================================

        self.action_engine = ActionEngine()

    # ==========================================================
    # WAIT FOR WAKE WORD
    # ==========================================================

    def wait_for_wake_word(self):

        text = self.stt.listen()

        if not text:
            return False

        print()
        print("HEARD:")
        print(text)

        lower = text.lower()

        wake_words = [
            "hey nexus",
            "hey nexas",
            "hi nexus",
            "hello nexus",
            "nexus",
        ]

        for wake_word in wake_words:

            if wake_word in lower:

                print()
                print("🧠 NEXUS activated.")

                self.tts.speak(
                    "Hello Mubarak, how can I help you?"
                )

                return True

        return False

    # ==========================================================
    # HANDLE COMMAND
    # ==========================================================

    def handle_command(self):

        print()
        print("🎤 Listening for command...")

        text = self.stt.listen()

        if not text:
            return

        print()
        print("COMMAND:")
        print(text)

        # ======================================================
        # UNDERSTAND COMMAND
        # ======================================================

        print()
        print("🧠 NEXUS is understanding...")

        intent = self.intent_engine.detect(text)

        print()
        print("INTENT:")
        print(intent.type)

        print("TARGET:")
        print(intent.target)

        # ======================================================
        # LOCK SYSTEM
        # ======================================================

        if intent.type == IntentType.LOCK_SYSTEM:

            response = "Securing your system now."

            print()
            print("NEXUS:")
            print(response)

            # Speak BEFORE locking
            self.tts.speak(response)

            # Execute actual Windows action
            self.action_engine.execute(intent)

            return

        # ======================================================
        # CHAT
        # ======================================================

        if intent.type == IntentType.CHAT:

            print()
            print("🧠 NEXUS is thinking...")

            try:

                chunks = self.ai.ask_stream(text)

                reply_parts = []

                for chunk in chunks:

                    reply_parts.append(chunk)

                reply = "".join(
                    reply_parts
                ).strip()

            except Exception as e:

                print(
                    "AI ERROR:",
                    e
                )

                reply = (
                    "Sorry, I couldn't "
                    "connect to my AI engine."
                )

            print()
            print("NEXUS:")
            print(reply)

            print()
            print("🔊 Speaking...")

            self.tts.speak(reply)

            return

        # ======================================================
        # OTHER INTENTS
        # ======================================================

        print()
        print("⚠️ Action not implemented yet.")

        self.tts.speak(
            "I understand the command, "
            "but that action is not available yet."
        )

    # ==========================================================
    # OLD SINGLE INTERACTION
    # ==========================================================

    def listen_and_respond(self):

        self.handle_command()

    # ==========================================================
    # STOP
    # ==========================================================

    def stop(self):

        self.tts.stop()