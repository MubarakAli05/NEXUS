from src.core.intent.intent_engine import IntentEngine


engine = IntentEngine()


tests = [

    # English
    "lock the system",
    "open VS Code",
    "close Blender",
    "take a screenshot",

    # Tanglish
    "system lock pannu",
    "VS Code open pannu",
    "Blender close pannu",
    "screenshot eduthu",

    # Memory
    "remember that I use VS Code",
    "what do you remember about me",
    "forget my editor",

    # Normal conversation
    "explain Python to me",
]


print()
print("====================================")
print("        NEXUS INTENT TEST")
print("====================================")


for text in tests:

    result = engine.detect(text)

    print()
    print("INPUT:")
    print(text)

    print("INTENT:")
    print(result.type)

    print("TARGET:")
    print(result.target)

    print("VALUE:")
    print(result.value)

    print("CONFIDENCE:")
    print(result.confidence)