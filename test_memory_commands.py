from src.core.memory.memory_commands import MemoryCommand


tests = [
    "remember that my name is Mubarak",
    "remember that I use VS Code",
    "I prefer Python",
    "what do you remember about me",
    "forget my editor",
    "clear my memory",
]


print("================================")
print("   NEXUS MEMORY COMMAND TEST")
print("================================")


for text in tests:

    result = MemoryCommand.detect(text)

    print()
    print("INPUT:")
    print(text)

    print("RESULT:")
    print(result)


print()
print("================================")
print("       TEST COMPLETE")
print("================================")
print("\n\n=== MEMORY PARSING TEST ===")

memory_tests = [
    "my name is Mubarak",
    "I use VS Code",
    "I prefer Python",
    "my favorite language is Python",
]

for text in memory_tests:

    result = MemoryCommand.parse_memory(text)

    print()
    print("INPUT:")
    print(text)

    print("PARSED:")
    print(result)