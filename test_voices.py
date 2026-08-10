import pyttsx3


engine = pyttsx3.init()

voices = engine.getProperty("voices")

print()
print("================================")
print("       NEXUS VOICES")
print("================================")
print()

for index, voice in enumerate(voices):

    print(
        f"{index}: "
        f"{voice.name} "
        f"| ID: {voice.id}"
    )

print()