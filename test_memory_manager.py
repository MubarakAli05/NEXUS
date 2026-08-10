from src.core.memory.memory_manager import MemoryManager


memory = MemoryManager()


print("=== NEXUS MEMORY TEST ===")


# ----------------------------------------------------------
# SAVE
# ----------------------------------------------------------

print("\nSaving memories...")

memory.remember(
    "personal",
    "name",
    "Mubarak"
)

memory.remember(
    "preference",
    "programming_language",
    "Python"
)


# ----------------------------------------------------------
# RECALL
# ----------------------------------------------------------

print("\nRecalling name...")

print(
    "Name:",
    memory.recall("name")
)


print("\nRecalling programming language...")

print(
    "Language:",
    memory.recall(
        "programming_language"
    )
)


# ----------------------------------------------------------
# ALL MEMORIES
# ----------------------------------------------------------

print("\nAll memories:")

for item in memory.get_all_memories():

    print(item)


# ----------------------------------------------------------
# CLOSE
# ----------------------------------------------------------

memory.close()

print("\nMemory test complete.")