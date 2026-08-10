from src.core.ai.ai_engine import AIEngine


ai = AIEngine()

print("NEXUS:")
print()

for chunk in ai.ask_stream(
    "Explain Python in a simple way."
):

    print(
        chunk,
        end="",
        flush=True
    )

print("\n")

ai.close()