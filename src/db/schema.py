import sqlite3
from typing import Dict, Any


def get_database_schema(db_path: str = "sample_university.db") -> Dict[str, Any]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    schema: Dict[str, Any] = {}
    for (t,) in tables:
        cursor.execute(f"PRAGMA table_info({t})")
        cols = cursor.fetchall()
        schema[t] = {
            "columns": [
                {"name": c[1], "type": c[2], "primary_key": bool(c[5])} for c in cols
            ]
        }
    conn.close()
    return schema
