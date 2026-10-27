import re
import sqlite3
import time
from pathlib import Path

SEED_PATH = Path(__file__).resolve().parent.parent / "data" / "seed.sql"
FORBIDDEN = re.compile(
    r"\b(insert|update|delete|drop|alter|create|attach|detach|pragma|vacuum|reindex)\b",
    re.IGNORECASE,
)
MAX_ROWS = 200
TIMEOUT_SECONDS = 2


def create_connection():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.executescript(SEED_PATH.read_text(encoding="utf-8"))
    conn.execute("PRAGMA query_only = ON")
    return conn


def validate_query(sql):
    cleaned = sql.strip().rstrip(";").strip()
    if not cleaned:
        return "The query is empty."
    if ";" in cleaned:
        return "Only one statement is allowed."
    if not re.match(r"^(select|with)\b", cleaned, re.IGNORECASE):
        return "Only SELECT queries are allowed."
    match = FORBIDDEN.search(cleaned)
    if match:
        return f"The keyword {match.group(1).upper()} is not allowed."
    return None


def run_query(conn, sql):
    problem = validate_query(sql)
    if problem:
        return {"columns": [], "rows": [], "error": problem}
    cleaned = sql.strip().rstrip(";")
    deadline = time.monotonic() + TIMEOUT_SECONDS
    conn.set_progress_handler(lambda: 1 if time.monotonic() > deadline else 0, 10000)
    try:
        cursor = conn.execute(cleaned)
        columns = [item[0] for item in cursor.description] if cursor.description else []
        rows = cursor.fetchmany(MAX_ROWS)
        return {"columns": columns, "rows": rows, "error": None}
    except sqlite3.Error as exc:
        return {"columns": [], "rows": [], "error": str(exc)}
    finally:
        conn.set_progress_handler(None, 0)


def get_schema(conn):
    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
    ).fetchall()
    schema = {}
    for (table,) in tables:
        info = conn.execute(f"PRAGMA table_info({table})").fetchall()
        schema[table] = [(column[1], column[2]) for column in info]
    return schema
