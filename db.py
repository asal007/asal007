import sqlite3
import os
import json
from datetime import datetime
from pathlib import Path

# Stelle sicher, dass .streamlit-Verzeichnis existiert
db_dir = Path(".streamlit")
db_dir.mkdir(exist_ok=True)
DB_PATH = db_dir / "users.db"
USERS_JSON = db_dir / "users.json"

# Initialisiere Datenbankschema
def init_db():
    """Erstellt die Datenbankstruktur falls nicht vorhanden."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            totp_secret TEXT,
            is_admin INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS reset_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            token TEXT UNIQUE NOT NULL,
            expires_at TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS rate_limits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            endpoint TEXT NOT NULL,
            attempt_count INTEGER DEFAULT 1,
            first_attempt TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            title TEXT,
            price REAL,
            location TEXT,
            sqm REAL,
            energy_class TEXT,
            condition TEXT,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            category TEXT,
            text TEXT,
            done INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    """)
    
    conn.commit()
    conn.close()
    
    # Migriere alte users.json falls vorhanden
    migrate_users_json()


def migrate_users_json():
    """Migriert Benutzer von users.json zu users.db (einmalig)."""
    if not USERS_JSON.exists():
        return
    
    try:
        with open(USERS_JSON, "r") as f:
            old_users = json.load(f)
    except Exception:
        return
    
    # Prüfe ob bereits migiert
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    count = c.fetchone()[0]
    conn.close()
    
    if count > 0:
        return  # Bereits vorhanden
    
    # Migriere jeden Benutzer
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    for username, data in old_users.items():
        try:
            pwd_hash = data.get("password", "")
            email = data.get("email", "")
            is_admin = 1 if data.get("is_admin", False) else 0
            
            c.execute(
                "INSERT INTO users (username, password_hash, email, is_admin) VALUES (?, ?, ?, ?)",
                (username, pwd_hash, email, is_admin)
            )
        except Exception:
            pass  # Skip bei Fehlern
    
    conn.commit()
    conn.close()


# Funktionen für Benutzerverwaltung
def get_user(username: str) -> dict:
    """Holt einen Benutzer aus der DB."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    
    if not row:
        return None
    
    return {
        "id": row[0],
        "username": row[1],
        "password_hash": row[2],
        "email": row[3],
        "totp_secret": row[4],
        "is_admin": row[5],
        "created_at": row[6],
        "updated_at": row[7],
    }


def check_user_exists(username: str) -> bool:
    """Prüft ob Benutzer existiert."""
    return get_user(username) is not None


def add_user(username: str, password_hash: str, email: str = "", is_admin: bool = False):
    """Fügt neuen Benutzer hinzu."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        c.execute(
            "INSERT INTO users (username, password_hash, email, is_admin) VALUES (?, ?, ?, ?)",
            (username, password_hash, email, 1 if is_admin else 0)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Benutzer existiert bereits
    finally:
        conn.close()


def update_user_password(username: str, password_hash: str, totp_secret: str = None):
    """Updated Passwort und optional TOTP für einen Benutzer."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    if totp_secret:
        c.execute(
            "UPDATE users SET password_hash = ?, totp_secret = ?, updated_at = CURRENT_TIMESTAMP WHERE username = ?",
            (password_hash, totp_secret, username)
        )
    else:
        c.execute(
            "UPDATE users SET password_hash = ?, updated_at = CURRENT_TIMESTAMP WHERE username = ?",
            (password_hash, username)
        )
    
    conn.commit()
    conn.close()


def update_user_email(username: str, email: str):
    """Updated E-Mail-Adresse für einen Benutzer."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "UPDATE users SET email = ?, updated_at = CURRENT_TIMESTAMP WHERE username = ?",
        (email, username)
    )
    conn.commit()
    conn.close()


def set_admin(username: str, is_admin: bool):
    """Setzt Admin-Status für einen Benutzer."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "UPDATE users SET is_admin = ?, updated_at = CURRENT_TIMESTAMP WHERE username = ?",
        (1 if is_admin else 0, username)
    )
    conn.commit()
    conn.close()


def delete_user(username: str):
    """Löscht einen Benutzer."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE username = ?", (username,))
    c.execute("DELETE FROM reset_tokens WHERE username = ?", (username,))
    conn.commit()
    conn.close()


def list_all_users() -> list:
    """Listet alle Benutzer auf."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT username, email, is_admin, created_at FROM users ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    
    return [
        {
            "username": row[0],
            "email": row[1],
            "is_admin": bool(row[2]),
            "created_at": row[3],
        }
        for row in rows
    ]


# Reset-Token Verwaltung
def get_reset_token(username: str) -> dict:
    """Holt den Reset-Token für einen Benutzer."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT token, expires_at FROM reset_tokens WHERE username = ? AND expires_at > CURRENT_TIMESTAMP LIMIT 1",
        (username,)
    )
    row = c.fetchone()
    conn.close()
    
    if not row:
        return None
    
    return {"token": row[0], "expires_at": row[1]}


def set_reset_token(username: str, token: str, expires_at: str):
    """Speichert einen Reset-Token."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Lösche alte Tokens
    c.execute("DELETE FROM reset_tokens WHERE username = ?", (username,))
    
    # Speichere neuen Token falls vorhanden
    if token and expires_at:
        c.execute(
            "INSERT INTO reset_tokens (username, token, expires_at) VALUES (?, ?, ?)",
            (username, token, expires_at)
        )
    
    conn.commit()
    conn.close()


def verify_reset_token(username: str, token: str) -> bool:
    """Verifiziert einen Reset-Token."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT 1 FROM reset_tokens WHERE username = ? AND token = ? AND expires_at > CURRENT_TIMESTAMP",
        (username, token)
    )
    result = c.fetchone()
    conn.close()
    
    return result is not None


# Rate Limiting für Brute-Force-Schutz
def check_rate_limit(username: str, endpoint: str = "login", max_attempts: int = 5, window_minutes: int = 15) -> bool:
    """
    Prüft ob Benutzer Rate-Limit überschritten hat.
    Gibt True zurück falls OK, False falls zu viele Versuche.
    """
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Lösche alte Einträge
    c.execute("""
        DELETE FROM rate_limits 
        WHERE username = ? AND endpoint = ? 
        AND datetime(first_attempt, '+' || ? || ' minutes') < CURRENT_TIMESTAMP
    """, (username, endpoint, window_minutes))
    
    # Prüfe aktuelle Versuche
    c.execute(
        "SELECT attempt_count FROM rate_limits WHERE username = ? AND endpoint = ?",
        (username, endpoint)
    )
    row = c.fetchone()
    
    if not row:
        # Neuer Versuch
        c.execute(
            "INSERT INTO rate_limits (username, endpoint) VALUES (?, ?)",
            (username, endpoint)
        )
    else:
        if row[0] >= max_attempts:
            conn.close()
            return False
        
        # Erhöhe Zähler
        c.execute(
            "UPDATE rate_limits SET attempt_count = attempt_count + 1 WHERE username = ? AND endpoint = ?",
            (username, endpoint)
        )
    
    conn.commit()
    conn.close()
    return True


# Favoriten-Management
def add_favorite(username: str, title: str, price: float, location: str, sqm: float, energy_class: str, condition: str, notes: str = ""):
    """Fügt einen Favoriten hinzu."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO favorites (username, title, price, location, sqm, energy_class, condition, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (username, title, price, location, sqm, energy_class, condition, notes)
    )
    conn.commit()
    conn.close()


def get_favorites(username: str) -> list:
    """Holt alle Favoriten eines Benutzers."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, price, location, sqm, energy_class, condition, notes FROM favorites WHERE username = ? ORDER BY created_at DESC", (username,))
    rows = c.fetchall()
    conn.close()
    
    return [
        {
            "id": row[0],
            "title": row[1],
            "price": row[2],
            "location": row[3],
            "sqm": row[4],
            "energy_class": row[5],
            "condition": row[6],
            "notes": row[7],
        }
        for row in rows
    ]


def delete_favorite(fav_id: int):
    """Löscht einen Favoriten."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM favorites WHERE id = ?", (fav_id,))
    conn.commit()
    conn.close()


# To-Do-Management
def add_todo(username: str, category: str, text: str):
    """Fügt ein To-Do hinzu."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO todos (username, category, text) VALUES (?, ?, ?)",
        (username, category, text)
    )
    conn.commit()
    conn.close()


def get_todos(username: str, category: str = None) -> list:
    """Holt To-Dos eines Benutzers, optional nach Kategorie gefiltert."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    if category:
        c.execute("SELECT id, category, text, done FROM todos WHERE username = ? AND category = ? ORDER BY created_at", (username, category))
    else:
        c.execute("SELECT id, category, text, done FROM todos WHERE username = ? ORDER BY created_at", (username,))
    
    rows = c.fetchall()
    conn.close()
    
    return [
        {
            "id": row[0],
            "category": row[1],
            "text": row[2],
            "done": bool(row[3]),
        }
        for row in rows
    ]


def update_todo_status(todo_id: int, done: bool):
    """Updated Status eines To-Dos."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE todos SET done = ? WHERE id = ?", (1 if done else 0, todo_id))
    conn.commit()
    conn.close()


def delete_todo(todo_id: int):
    """Löscht ein To-Do."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()


# Initialisiere DB beim Import
init_db()
