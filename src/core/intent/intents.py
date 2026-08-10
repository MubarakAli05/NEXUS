from enum import Enum
from dataclasses import dataclass
from typing import Optional


class IntentType(Enum):

    CHAT = "chat"

    LOCK_SYSTEM = "lock_system"

    SYSTEM_INFO = "system_info"

    TAKE_SCREENSHOT = "take_screenshot"

    OPEN_APP = "open_app"

    CLOSE_APP = "close_app"

    REMEMBER = "remember"

    FORGET = "forget"

    LIST_MEMORY = "list_memory"

    UNKNOWN = "unknown"


@dataclass
class Intent:

    type: IntentType

    target: Optional[str] = None

    value: Optional[str] = None

    confidence: float = 1.0