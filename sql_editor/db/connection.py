import sqlite3
from typing import Any, List, Tuple


class Database:
    """Простая обёртка над SQLite: подключение и выполнение SELECT-запросов."""

    def __init__(self) -> None:
        self._conn = None
        self._path = None

    def connect(self, path: str) -> None:
        if self._conn is not None:
            self._conn.close()
        self._conn = sqlite3.connect(path)
        self._path = path

    def is_connected(self) -> bool:
        return self._conn is not None

    @property
    def path(self) -> str | None:
        return self._path

    def execute_select(self, query: str) -> tuple[List[str], List[Tuple[Any, ...]]]:
        if self._conn is None:
            raise RuntimeError("База данных не подключена")

        cursor = self._conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        col_names = [d[0] for d in cursor.description] if cursor.description else []
        cursor.close()
        return col_names, rows

    def get_tables(self) -> list[str]:
        if not self._conn:
            raise RuntimeError("База данных не подключена")
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = [r[0] for r in cursor.fetchall()]
        cursor.close()
        return tables

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None
            self._path = None
