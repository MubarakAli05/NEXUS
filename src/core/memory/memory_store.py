import sqlite3
from pathlib import Path


class MemoryStore:

    def __init__(self):

        self.data_dir = Path("data")

        self.data_dir.mkdir(
            exist_ok=True
        )

        self.database = (
            self.data_dir / "nexus_memory.db"
        )

        self.connection = sqlite3.connect(
            self.database,
            check_same_thread=False
        )

        self._create_tables()

    # ==========================================================
    # CREATE TABLE
    # ==========================================================

    def _create_tables(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.connection.commit()

    # ==========================================================
    # SAVE
    # ==========================================================

    def save(
        self,
        category: str,
        key: str,
        value: str
    ):

        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO memories (
                category,
                key,
                value
            )
            VALUES (?, ?, ?)
        """, (
            category,
            key,
            value
        ))

        self.connection.commit()

    # ==========================================================
    # GET BY KEY
    # ==========================================================

    def get(self, key: str):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT value
            FROM memories
            WHERE key = ?
            ORDER BY id DESC
            LIMIT 1
        """, (key,))

        result = cursor.fetchone()

        if result:
            return result[0]

        return None

    # ==========================================================
    # FIND BY KEY
    # ==========================================================

    def find_by_key(self, key: str):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT
                id,
                category,
                key,
                value,
                created_at
            FROM memories
            WHERE key = ?
            ORDER BY id DESC
        """, (key,))

        return cursor.fetchall()

    # ==========================================================
    # DELETE BY KEY
    # ==========================================================

    def delete_by_key(self, key: str):

        cursor = self.connection.cursor()

        cursor.execute("""
            DELETE FROM memories
            WHERE key = ?
        """, (key,))

        deleted = cursor.rowcount

        self.connection.commit()

        return deleted

    # ==========================================================
    # GET ALL
    # ==========================================================

    def get_all(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT
                id,
                category,
                key,
                value,
                created_at
            FROM memories
            ORDER BY id DESC
        """)

        return cursor.fetchall()

    # ==========================================================
    # DELETE BY ID
    # ==========================================================

    def delete(self, memory_id: int):

        cursor = self.connection.cursor()

        cursor.execute("""
            DELETE FROM memories
            WHERE id = ?
        """, (memory_id,))

        deleted = cursor.rowcount

        self.connection.commit()

        return deleted

    # ==========================================================
    # CLEAR ALL
    # ==========================================================

    def clear(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            DELETE FROM memories
        """)

        deleted = cursor.rowcount

        self.connection.commit()

        return deleted

    # ==========================================================
    # CLOSE
    # ==========================================================

    def close(self):

        self.connection.close()