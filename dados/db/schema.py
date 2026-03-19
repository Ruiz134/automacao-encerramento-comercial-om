from __future__ import annotations

import sqlite3

def init_schema(cursor: sqlite3.Connection) -> None:
    cursor.execute("""CREATE TABLE IF NOT EXISTS ordens_para_encerrar (
               id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
               Ordens TEXT NOT NULL UNIQUE               
    )""")

    cursor.commit()
