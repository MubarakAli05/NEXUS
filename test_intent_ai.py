import json

import ollama


MODEL = "qwen3:4b-instruct"


SYSTEM_PROMPT = """
You are the intent parser for NEXUS, a personal AI assistant.

Your job is ONLY to understand the user's command and convert it
into a JSON object.

Supported intents:

- chat
- lock_system
- open_app
- close_app
- take_screenshot
- system_info
- remember
- forget
- list_memory

Rules:

1. Understand English, Tamil, Tanglish, and mixed English/Tamil.
2. Understand natural variations and imperfect phrasing.
3. Do NOT execute anything.
4. Return ONLY valid JSON.
5. Never add explanations outside JSON.

For OPEN_APP and CLOSE_APP, include the application name in "target".

Examples:

User:
"lock the system"

JSON:
{"intent":"lock_system","target":null}

User:
"system lock pannu"

JSON:
{"intent":"lock_system","target":null}

User:
"VS Code open pannu"

JSON:
{"intent":"open_app","target":"VS Code"}

User:
"Blender close pannidu"

JSON:
{"intent":"close_app","target":"Blender"}

User:
"take a screenshot"

JSON:
{"intent":"take_screenshot","target":null}

User:
"explain Python"

JSON:
{"intent":"chat","target":null}
"""


tests = [
    "hey nexus can you please lock my computer",
    "system-ah lock pannidu",
    "VS Code open pannu",
    "Blender close pannidu",
    "enakku oru screenshot eduthu",
    "explain Python to me",
]


print("======================================")
print("       NEXUS AI INTENT TEST")
print("======================================")


for text in tests:

    print()
    print("INPUT:")
    print(text)

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": text,
            },
        ],
        format="json",
    )

    raw = response["message"]["content"]

    print()
    print("RAW:")
    print(raw)

    try:

        result = json.loads(raw)

        print()
        print("PARSED:")
        print(result)

    except json.JSONDecodeError:

        print()
        print("❌ INVALID JSON")