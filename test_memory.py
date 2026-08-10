from src.core.memory.memory_store import MemoryStore


memory = MemoryStore()


print("Saving memory...")

memory.save(
    "personal",
    "name",
    "Mubarak"
)


print("Reading memory...")

name = memory.get("name")

print("Name:", name)


print("\nAll memories:")

for item in memory.get_all():

    print(item)


memory.close()