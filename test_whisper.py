import sounddevice as sd
import numpy as np

from faster_whisper import WhisperModel


print("======================================")
print("        NEXUS WHISPER TEST")
print("======================================")

print()
print("Loading Whisper model...")


model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)


print("Whisper ready.")
print()
print("Speak for about 5 seconds.")
print()


sample_rate = 16000
duration = 5


audio = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="float32"
)

sd.wait()


audio = np.squeeze(audio)


print()
print("🧠 Transcribing...")


segments, info = model.transcribe(
    audio,
    beam_size=5,
    language=None,
    task="translate"
)

text = ""

for segment in segments:

    text += segment.text


text = text.strip()


print()
print("LANGUAGE:")
print(info.language)

print()
print("YOU:")
print(text)

print()
print("======================================")
print("          TEST COMPLETE")
print("======================================")