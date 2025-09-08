import sqlite3

cursor: sqlite3.Cursor | None = None
conn: sqlite3.Connection | None = None


def get_conn() -> sqlite3.Connection:
    global conn
    if conn is None:
        conn = sqlite3.connect("history.db")
    return conn


def get_cursor() -> sqlite3.Cursor:
    global cursor
    if cursor is None:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS request(expression TEXT)")
    return cursor


def commit() -> None:
    get_conn().commit()
