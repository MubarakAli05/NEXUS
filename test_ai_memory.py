from src.core.ai.ai_engine import AIEngine


ai = AIEngine()


print("================================")
print("       NEXUS MEMORY TEST")
print("================================")


# ==========================================================
# SHOW CURRENT MEMORY
# ==========================================================

print("\nStored name:")

print(
    ai.recall("name")
)


print("\nStored programming language:")

print(
    ai.recall(
        "programming_language"
    )
)


# ==========================================================
# ASK AI
# ==========================================================

print("\nNEXUS:")

reply = ai.ask(
    "What programming language do I prefer?"
)

print(reply)


# ==========================================================
# ADD NEW MEMORY
# ==========================================================

print("\nSaving new memory...")

ai.remember(
    "preference",
    "editor",
    "VS Code"
)


print(
    "Editor:",
    ai.recall("editor")
)


# ==========================================================
# ASK AGAIN
# ==========================================================

print("\nNEXUS:")

reply = ai.ask(
    "What editor do I prefer?"
)

print(reply)


# ==========================================================
# CLOSE
# ==========================================================

ai.close()

print("\n================================")
print("       TEST COMPLETE")
print("================================")