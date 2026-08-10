import pyttsx3


class TextToSpeech:

    def __init__(self):

        self.engine = pyttsx3.init()

        # ==================================================
        # VOICE SETTINGS
        # ==================================================

        self.engine.setProperty(
            "rate",
            175
        )

        self.engine.setProperty(
            "volume",
            1.0
        )

        # ==================================================
        # FIND ENGLISH VOICE
        # ==================================================

        voices = self.engine.getProperty(
            "voices"
        )

        for voice in voices:

            name = (
                getattr(voice, "name", "")
                or ""
            ).lower()

            languages = (
                getattr(voice, "languages", [])
                or []
            )

            if (
                "english" in name
                or "en_" in name
                or "en-" in name
            ):

                self.engine.setProperty(
                    "voice",
                    voice.id
                )

                break

    # ==================================================
    # SPEAK
    # ==================================================

    def speak(self, text: str):

        if not text:
            return

        self.engine.say(text)

        self.engine.runAndWait()

    # ==================================================
    # STOP
    # ==================================================

    def stop(self):

        self.engine.stop()