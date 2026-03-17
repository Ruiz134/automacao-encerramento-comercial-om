# utils/db.py
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional, Iterable, Sequence, Any
import pandas as pd

import utils.config as cfg

def get_db_path() -> Path:
    base = cfg.DATA_DIR_SQL.resolve()
    base.mkdir(parents=True, exist_ok=True)
    return base / "sap_extracts.db"


def connect(db_path: Optional[Path] = None) -> sqlite3.Connection:
    db_path = db_path or get_db_path()
    conn = sqlite3.connect(db_path.as_posix())
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    return df


def ensure_cols(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    df = df.copy()
    for c in cols:
        if c not in df.columns:
            df[c] = None
    return df[cols]


def chunks(seq: Sequence, size: int) -> Iterable[Sequence]:
    for i in range(0, len(seq), size):
        yield seq[i:i + size]

# =========================
# Normalizadores robustos
# =========================
def to_id_str(x: Any) -> Optional[str]:
    if x is None or (isinstance(x, float) and pd.isna(x)) or pd.isna(x):
        return None

    if isinstance(x, (bytes, bytearray, memoryview)):
        b = bytes(x)
        try:
            s = b.decode("utf-8", errors="ignore").strip()
            if s:
                digits = "".join(ch for ch in s if ch.isdigit())
                if digits:
                    return digits
        except Exception:
            pass

        try:
            val = int.from_bytes(b, byteorder="little", signed=False)
            if val == 0:
                return None
            return str(val)
        except Exception:
            return None

    if isinstance(x, int):
        return str(x)

    if isinstance(x, float):
        try:
            return str(int(x))
        except Exception:
            return str(x).replace(".0", "").strip()

    s = str(x).strip()
    if s.lower() in {"<na>", "nan", "none", ""}:
        return None

    if "." in s:
        left, right = s.split(".", 1)
        if right.isdigit() and set(right) <= {"0"}:
            s = left

    digits = "".join(ch for ch in s if ch.isdigit())
    return digits if digits else s


def to_int_id(x: Any) -> Optional[int]:
    s = to_id_str(x)
    if not s:
        return None
    try:
        return int(s)
    except Exception:
        return None