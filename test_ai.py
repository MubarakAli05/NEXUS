from src.core.ai.ai_engine import AIEngine

ai = AIEngine()

print("===================================")
print("        NEXUS AI TEST")
print("Type 'exit' to quit.")
print("===================================\n")

while True:

    user = input("You: ")

    if user.lower() == "exit":
        break

    reply = ai.ask(user)

    print("\nNEXUS:")
    print(reply)
    print()