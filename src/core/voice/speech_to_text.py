import queue

import numpy as np
import sounddevice as sd

from faster_whisper import WhisperModel


class SpeechToText:

    def __init__(
        self,
        model_size="small"
    ):

        print("🧠 Loading Whisper...")

        self.model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8"
        )

        self.sample_rate = 16000

        self.audio_queue = queue.Queue()

        self.running = False

        print("✓ Whisper ready.")

    # ==========================================================
    # AUDIO CALLBACK
    # ==========================================================

    def _callback(
        self,
        indata,
        frames,
        time,
        status
    ):

        if status:

            print(
                "Audio:",
                status
            )

        if self.running:

            self.audio_queue.put(
                indata.copy()
            )

    # ==========================================================
    # CLEAR OLD AUDIO
    # ==========================================================

    def _clear_queue(self):

        while not self.audio_queue.empty():

            try:

                self.audio_queue.get_nowait()

            except queue.Empty:

                break

    # ==========================================================
    # LISTEN
    # ==========================================================

    def listen(self):

        print()
        print("🎤 Listening...")

        self._clear_queue()

        self.running = True

        audio_chunks = []

        try:

            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype="float32",
                blocksize=4000,
                callback=self._callback
            ):

                # ----------------------------------------------
                # Record for now
                # ----------------------------------------------

                duration = 5

                for _ in range(
                    int(
                        self.sample_rate
                        * duration
                        / 4000
                    )
                ):

                    try:

                        chunk = (
                            self.audio_queue.get(
                                timeout=1
                            )
                        )

                        audio_chunks.append(
                            chunk
                        )

                    except queue.Empty:

                        continue

        except KeyboardInterrupt:

            self.running = False

            print(
                "\n🛑 Voice listening stopped."
            )

            raise

        finally:

            self.running = False

        # ======================================================
        # NO AUDIO
        # ======================================================

        if not audio_chunks:

            return ""

        # ======================================================
        # COMBINE AUDIO
        # ======================================================

        audio = np.concatenate(
            audio_chunks,
            axis=0
        )

        audio = np.squeeze(
            audio
        )

        # ======================================================
        # WHISPER
        # ======================================================

        print()
        print("🧠 Transcribing...")

        segments, info = self.model.transcribe(
            audio,
            beam_size=5,
            language=None,
            task="translate"
        )

        text_parts = []

        for segment in segments:

            text_parts.append(
                segment.text
            )

        text = " ".join(
            text_parts
        ).strip()

        # ======================================================
        # RESULT
        # ======================================================

        if text:

            print()
            print("🎤 Heard:")
            print(text)

        return text