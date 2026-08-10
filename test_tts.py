import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty("voices")

for i, voice in enumerate(voices):

    print(f"\nTesting {i}: {voice.name}")

    try:
        engine.setProperty("voice", voice.id)

        engine.say(
            f"Hello Mubarak. "
            f"This is voice number {i}."
        )

        engine.runAndWait()

        print("Finished.")

    except Exception as e:
        print("ERROR:", e)