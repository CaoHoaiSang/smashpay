import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get("DATA_DIR", BASE_DIR / "data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "badminton.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


@contextmanager
def db_cursor():
    conn = get_connection()
    try:
        cur = conn.cursor()
        yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    with db_cursor() as cur:
        cur.executescript(
            """
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                bank_id TEXT DEFAULT '',
                account_no TEXT DEFAULT '',
                account_name TEXT DEFAULT '',
                is_regular INTEGER NOT NULL DEFAULT 1,
                is_active INTEGER NOT NULL DEFAULT 1,
                default_payer_id INTEGER DEFAULT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
                FOREIGN KEY (default_payer_id) REFERENCES members(id) ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                played_at TEXT NOT NULL,
                parking_fee INTEGER NOT NULL DEFAULT 5000,
                notes TEXT DEFAULT '',
                status TEXT NOT NULL DEFAULT 'open',
                is_template INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
                updated_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
            );

            CREATE TABLE IF NOT EXISTS session_participants (
                session_id INTEGER NOT NULL,
                member_id INTEGER NOT NULL,
                payer_member_id INTEGER DEFAULT NULL,
                PRIMARY KEY (session_id, member_id),
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE,
                FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE,
                FOREIGN KEY (payer_member_id) REFERENCES members(id) ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                category TEXT NOT NULL,          -- court | shuttle | parking | snack | drink | other
                title TEXT NOT NULL,
                split_type TEXT NOT NULL,        -- equal_split | parking | itemized
                payer_id INTEGER,                -- nullable when parking is included_in_court
                total_amount INTEGER NOT NULL DEFAULT 0,
                parking_mode TEXT DEFAULT NULL,  -- separate_payer | included_in_court
                unit_fee INTEGER DEFAULT 5000,
                created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE,
                FOREIGN KEY (payer_id) REFERENCES members(id) ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS expense_participants (
                expense_id INTEGER NOT NULL,
                member_id INTEGER NOT NULL,
                PRIMARY KEY (expense_id, member_id),
                FOREIGN KEY (expense_id) REFERENCES expenses(id) ON DELETE CASCADE,
                FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS expense_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expense_id INTEGER NOT NULL,
                item_name TEXT NOT NULL DEFAULT '',
                amount INTEGER NOT NULL DEFAULT 0,
                pricing_mode TEXT NOT NULL DEFAULT 'per_person', -- per_person | split_total
                FOREIGN KEY (expense_id) REFERENCES expenses(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS expense_item_participants (
                item_id INTEGER NOT NULL,
                member_id INTEGER NOT NULL,
                PRIMARY KEY (item_id, member_id),
                FOREIGN KEY (item_id) REFERENCES expense_items(id) ON DELETE CASCADE,
                FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS settlements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                from_member_id INTEGER NOT NULL,
                to_member_id INTEGER NOT NULL,
                amount INTEGER NOT NULL,
                is_paid INTEGER NOT NULL DEFAULT 0,
                paid_at TEXT DEFAULT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE,
                FOREIGN KEY (from_member_id) REFERENCES members(id) ON DELETE CASCADE,
                FOREIGN KEY (to_member_id) REFERENCES members(id) ON DELETE CASCADE
            );
            """
        )

        # Migration: Add default_payer_id to members if missing
        try:
            cur.execute("ALTER TABLE members ADD COLUMN default_payer_id INTEGER DEFAULT NULL REFERENCES members(id) ON DELETE SET NULL")
        except sqlite3.OperationalError:
            pass

        # Migration: Add payer_member_id to session_participants if missing
        try:
            cur.execute("ALTER TABLE session_participants ADD COLUMN payer_member_id INTEGER DEFAULT NULL REFERENCES members(id) ON DELETE SET NULL")
        except sqlite3.OperationalError:
            pass

        # Migration: Mark one session as the reusable default form
        try:
            cur.execute("ALTER TABLE sessions ADD COLUMN is_template INTEGER NOT NULL DEFAULT 0")
        except sqlite3.OperationalError:
            pass
