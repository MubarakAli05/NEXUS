from src.core.voice.speech_to_text import SpeechToText
from src.core.intent.intent_engine import IntentEngine


print("======================================")
print("     NEXUS VOICE → INTENT TEST")
print("======================================")


stt = SpeechToText()

engine = IntentEngine()


text = stt.listen()


print()
print("VOICE TEXT:")
print(text)


if text:

    print()
    print("🧠 Understanding...")

    intent = engine.detect(text)

    print()
    print("INTENT:")
    print(intent.type)

    print()
    print("TARGET:")
    print(intent.target)

    print()
    print("CONFIDENCE:")
    print(intent.confidence)


print()
print("======================================")
print("             COMPLETE")
print("======================================")