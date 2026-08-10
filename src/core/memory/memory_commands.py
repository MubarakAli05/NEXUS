import re


class MemoryCommand:

    # ==========================================================
    # DETECT MEMORY COMMAND
    # ==========================================================

    @staticmethod
    def detect(message: str):

        if not message:
            return None

        text = message.strip()

        lower = text.lower()

        # ======================================================
        # REMEMBER
        # ======================================================

        remember_patterns = [
            r"^remember that (.+)$",
            r"^remember (.+)$",
            r"^save that (.+)$",
            r"^save (.+)$",
        ]

        for pattern in remember_patterns:

            match = re.match(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                content = match.group(1).strip()

                return {
                    "action": "remember",
                    "content": content
                }

        # ======================================================
        # DIRECT PREFERENCE
        # ======================================================

        preference_patterns = [
            r"^i prefer (.+)$",
            r"^i use (.+)$",
            r"^my favorite (.+?) is (.+)$",
        ]

        for pattern in preference_patterns:

            match = re.match(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                return {
                    "action": "remember",
                    "content": text
                }

        # ======================================================
        # WHAT DO YOU REMEMBER?
        # ======================================================

        recall_patterns = [
            "what do you remember",
            "what do you know about me",
            "show my memories",
            "show what you remember",
            "list my memories",
        ]

        for pattern in recall_patterns:

            if pattern in lower:

                return {
                    "action": "list"
                }

        # ======================================================
        # FORGET
        # ======================================================

        forget_match = re.match(
            r"^forget (.+)$",
            text,
            re.IGNORECASE
        )

        if forget_match:

            return {
                "action": "forget",
                "content": forget_match.group(1).strip()
            }

        # ======================================================
        # CLEAR MEMORY
        # ======================================================

        clear_patterns = [
            "clear my memory",
            "clear all memories",
            "delete all memories",
            "forget everything",
        ]

        for pattern in clear_patterns:

            if pattern in lower:

                return {
                    "action": "clear"
                }

        return None

    # ==========================================================
    # PARSE MEMORY
    # ==========================================================

    @staticmethod
    def parse_memory(content: str):

        content = content.strip()

        # ------------------------------------------------------
        # MY NAME IS...
        # ------------------------------------------------------

        match = re.match(
            r"my name is (.+)",
            content,
            re.IGNORECASE
        )

        if match:

            return (
                "personal",
                "name",
                match.group(1).strip()
            )

        # ------------------------------------------------------
        # I USE...
        # ------------------------------------------------------

        match = re.match(
            r"i use (.+)",
            content,
            re.IGNORECASE
        )

        if match:

            return (
                "preference",
                "tool",
                match.group(1).strip()
            )

        # ------------------------------------------------------
        # I PREFER...
        # ------------------------------------------------------

        match = re.match(
            r"i prefer (.+)",
            content,
            re.IGNORECASE
        )

        if match:

            return (
                "preference",
                "preference",
                match.group(1).strip()
            )

        # ------------------------------------------------------
        # MY FAVORITE ... IS ...
        # ------------------------------------------------------

        match = re.match(
            r"my favorite (.+?) is (.+)",
            content,
            re.IGNORECASE
        )

        if match:

            category = match.group(1).strip()

            value = match.group(2).strip()

            key = (
                "favorite_"
                + category.lower().replace(
                    " ",
                    "_"
                )
            )

            return (
                "preference",
                key,
                value
            )

        # ------------------------------------------------------
        # GENERIC MEMORY
        # ------------------------------------------------------

        return (
            "general",
            "note",
            content
        )