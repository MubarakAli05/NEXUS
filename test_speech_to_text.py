from src.core.voice.speech_to_text import SpeechToText


print("======================================")
print("       NEXUS SPEECH TEST")
print("======================================")

stt = SpeechToText()

text = stt.listen()

print()
print("FINAL TEXT:")
print(text)

print()
print("======================================")
print("          TEST COMPLETE")
print("======================================")