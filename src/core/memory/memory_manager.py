from src.core.memory.memory_store import MemoryStore


class MemoryManager:

    def __init__(self):

        self.store = MemoryStore()

    # ==========================================================
    # REMEMBER
    # ==========================================================

    def remember(
        self,
        category: str,
        key: str,
        value: str
    ):

        if not key or not value:
            return False

        self.store.save(
            category,
            key,
            value
        )

        return True

    # ==========================================================
    # RECALL
    # ==========================================================

    def recall(self, key: str):

        if not key:
            return None

        return self.store.get(key)

    # ==========================================================
    # FIND
    # ==========================================================

    def find(self, key: str):

        if not key:
            return []

        return self.store.find_by_key(key)

    # ==========================================================
    # FORGET BY KEY
    # ==========================================================

    def forget_by_key(self, key: str):

        if not key:
            return 0

        return self.store.delete_by_key(key)

    # ==========================================================
    # FORGET BY ID
    # ==========================================================

    def forget(self, memory_id: int):

        return self.store.delete(
            memory_id
        )

    # ==========================================================
    # ALL MEMORIES
    # ==========================================================

    def get_all_memories(self):

        return self.store.get_all()

    # ==========================================================
    # CLEAR ALL
    # ==========================================================

    def clear_all(self):

        return self.store.clear()

    # ==========================================================
    # CLOSE
    # ==========================================================

    def close(self):

        self.store.close()