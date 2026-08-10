import json
import ollama

from src.core.intent.intents import (
    Intent,
    IntentType,
)


class IntentEngine:

    def __init__(self, model="qwen3:4b"):

        self.model = model

    # ==========================================================
    # MAIN DETECTION
    # ==========================================================

    def detect(self, text: str) -> Intent:

        if not text:

            return Intent(
                type=IntentType.UNKNOWN,
                confidence=0.0
            )

        text = text.strip()

        # ------------------------------------------------------
        # FIRST: FAST RULE-BASED DETECTION
        # ------------------------------------------------------

        rule_result = self._rule_detect(text)

        if rule_result is not None:

            return rule_result

        # ------------------------------------------------------
        # SECOND: QWEN FALLBACK
        # ------------------------------------------------------

        return self._ai_detect(text)

    # ==========================================================
    # RULE ENGINE
    # ==========================================================

    def _rule_detect(self, text: str):

        lower = text.lower()

        # ======================================================
        # LOCK SYSTEM
        # ======================================================

        lock_words = [
            "lock the system",
            "lock system",
            "system lock",
            "lock my computer",
            "lock computer",
            "system lock pannu",
            "system ah lock pannu",
            "system-a lock pannu",
            "system ah lock pannidu",
            "system-a lock pannidu",
        ]

        if any(
            phrase in lower
            for phrase in lock_words
        ):

            return Intent(
                type=IntentType.LOCK_SYSTEM,
                confidence=0.95
            )

        # ======================================================
        # SCREENSHOT
        # ======================================================

        screenshot_words = [
            "take a screenshot",
            "take screenshot",
            "screenshot",
            "capture the screen",
            "screen shot eduthu",
            "screenshot eduthu",
        ]

        if any(
            phrase in lower
            for phrase in screenshot_words
        ):

            return Intent(
                type=IntentType.TAKE_SCREENSHOT,
                confidence=0.90
            )

        # ======================================================
        # APPLICATION COMMANDS
        # ======================================================

        # ------------------------------------------------------
        # OPEN APPLICATION
        # ------------------------------------------------------

        open_phrases = [
            "open pannu",
            "open pannidu",
            "open",
            "launch",
            "start",
            "run",
        ]

        for phrase in open_phrases:

            if phrase in lower:

                # Only use the simple rule when the command
                # actually starts with the phrase.

                if lower.startswith(phrase):

                    target = lower[
                        len(phrase):
                    ].strip()

                    if target.endswith(" pannu"):
                        target = target[:-6].strip()

                    if target.endswith(" pannidu"):
                        target = target[:-8].strip()

                    if target:

                        return Intent(
                            type=IntentType.OPEN_APP,
                            target=target,
                            confidence=0.85
                        )


        # ------------------------------------------------------
        # CLOSE APPLICATION
        # ------------------------------------------------------

        close_phrases = [
            "close pannu",
            "close pannidu",
            "close",
            "exit",
            "quit",
            "stop",
        ]

        for phrase in close_phrases:

            if phrase in lower:

                if lower.startswith(phrase):

                    target = lower[
                        len(phrase):
                    ].strip()

                    if target.endswith(" pannu"):
                        target = target[:-6].strip()

                    if target.endswith(" pannidu"):
                        target = target[:-8].strip()

                    if target:

                        return Intent(
                            type=IntentType.CLOSE_APP,
                            target=target,
                            confidence=0.85
                        )

                # ======================================================
                # MEMORY
                # ======================================================

                if (
                    lower.startswith("remember ")
                    or
                    lower.startswith("remember that ")
                ):

                    return Intent(
                        type=IntentType.REMEMBER,
                        value=text,
                        confidence=0.95
                    )

                # ======================================================
                # LIST MEMORY
                # ======================================================

                memory_questions = [
                    "what do you remember",
                    "what do you know about me",
                    "show my memories",
                    "show what you remember",
                ]

                if any(
                    phrase in lower
                    for phrase in memory_questions
                ):

                    return Intent(
                        type=IntentType.LIST_MEMORY,
                        confidence=0.95
                    )

                # ======================================================
                # FORGET
                # ======================================================

                if lower.startswith("forget "):

                    return Intent(
                        type=IntentType.FORGET,
                        value=text,
                        confidence=0.90
                    )

        # ======================================================
        # SYSTEM INFORMATION
        # ======================================================

        system_words = [
            "cpu usage",
            "ram usage",
            "memory usage",
            "disk usage",
            "system information",
            "system info",
            "how much ram",
            "how much cpu",
        ]

        if any(
            phrase in lower
            for phrase in system_words
        ):

            return Intent(
                type=IntentType.SYSTEM_INFO,
                target=text,
                confidence=0.85
            )

        # ======================================================
        # NO RULE MATCH
        # ======================================================

        return None

    # ==========================================================
    # QWEN AI DETECTION
    # ==========================================================

    def _ai_detect(self, text: str) -> Intent:

        system_prompt = """
You are the intent parser for NEXUS,
a personal AI assistant.

Your ONLY job is to understand the user's
request and return valid JSON.

Supported intents:

chat
lock_system
open_app
close_app
take_screenshot
system_info
remember
forget
list_memory

Rules:

1. Understand English.
2. Understand Tamil.
3. Understand Tanglish.
4. Understand mixed English and Tamil.
5. Understand natural variations.
6. Do not execute anything.
7. Return ONLY JSON.
8. For open_app and close_app,
   put the application name in target.
9. For chat, target should normally be null.

Examples:

"lock my computer"

{
    "intent": "lock_system",
    "target": null
}

"system-ah lock pannidu"

{
    "intent": "lock_system",
    "target": null
}

"VS Code open pannu"

{
    "intent": "open_app",
    "target": "VS Code"
}

"Blender close pannidu"

{
    "intent": "close_app",
    "target": "Blender"
}

"take a screenshot"

{
    "intent": "take_screenshot",
    "target": null
}

"explain Python"

{
    "intent": "chat",
    "target": null
}
"""

        try:

            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": text,
                    },
                ],
                format="json",
            )

            raw = response[
                "message"
            ][
                "content"
            ]

            data = json.loads(raw)

            intent_name = data.get(
                "intent",
                "unknown"
            )

            target = data.get(
                "target"
            )

            # --------------------------------------------------
            # CONVERT STRING → ENUM
            # --------------------------------------------------

            try:

                intent_type = IntentType(
                    intent_name
                )

            except ValueError:

                intent_type = IntentType.UNKNOWN

            # --------------------------------------------------
            # CONFIDENCE
            # --------------------------------------------------

            if intent_type == IntentType.UNKNOWN:

                confidence = 0.0

            else:

                confidence = 0.80

            return Intent(
                type=intent_type,
                target=target,
                confidence=confidence
            )

        except Exception as e:

            print(
                "Intent AI error:",
                e
            )

            return Intent(
                type=IntentType.UNKNOWN,
                confidence=0.0
            )