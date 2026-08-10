from src.core.intent.intent_engine import IntentEngine


engine = IntentEngine()


tests = [

    # Rule-based
    "lock the system",
    "open VS Code",
    "close Blender",

    # Tanglish
    "system lock pannu",

    # AI fallback
    "hey nexus can you please lock my computer",
    "could you launch Visual Studio Code for me",
    "please shut Blender down",
    "enakku oru screenshot eduthu",
    "system-ah lock pannidu",

    # Chat
    "explain quantum computing to me",
]


print()
print("======================================")
print("       NEXUS INTENT ENGINE TEST")
print("======================================")


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