from src.core.ai.ai_engine import AIEngine
from src.core.voice.voice_assistant import VoiceAssistant


print("======================================")
print("        NEXUS VOICE ASSISTANT")
print("======================================")

print()
print("Starting NEXUS...")

ai = AIEngine()

voice = VoiceAssistant(ai)

print("NEXUS is ready.")
print()
print("Say a command.")
print("Press Ctrl+C to stop.")
print()


try:

    while True:

        activated = voice.wait_for_wake_word()

        if activated:

            voice.handle_command()

except KeyboardInterrupt:

    print()
    print("Stopping NEXUS...")

    voice.stop()

    print("NEXUS offline.")