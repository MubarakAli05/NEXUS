from src.core.voice.speech_to_text import SpeechToText
from src.core.intent.intent_engine import IntentEngine
from src.core.actions.action_engine import ActionEngine


print("======================================")
print("     NEXUS VOICE → ACTION TEST")
print("======================================")


stt = SpeechToText()

intent_engine = IntentEngine()

action_engine = ActionEngine()


# ==========================================================
# LISTEN
# ==========================================================

text = stt.listen()


print()
print("VOICE TEXT:")
print(text)


if text:

    # ======================================================
    # UNDERSTAND
    # ======================================================

    print()
    print("🧠 Understanding...")

    intent = intent_engine.detect(text)


    print()
    print("INTENT:")
    print(intent.type)

    print()
    print("TARGET:")
    print(intent.target)

    print()
    print("CONFIDENCE:")
    print(intent.confidence)


    # ======================================================
    # ACTION
    # ======================================================

    print()
    print("⚡ Executing...")


    result = action_engine.execute(intent)


    print()
    print("ACTION RESULT:")
    print(result)


print()
print("======================================")
print("             COMPLETE")
print("======================================")