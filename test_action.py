from src.core.intent.intents import (
    Intent,
    IntentType,
)

from src.core.actions.action_engine import ActionEngine


print("======================================")
print("        NEXUS ACTION TEST")
print("======================================")

print()
print("Testing LOCK_SYSTEM...")
print()
print("The computer will lock in 3 seconds.")

import time

time.sleep(3)

intent = Intent(
    type=IntentType.LOCK_SYSTEM,
    confidence=1.0
)

engine = ActionEngine()

engine.execute(intent)