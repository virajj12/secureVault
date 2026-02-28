"""
SecureVault — Authentication Database Layer
Manages users table and login_logs table in SQLite.
"""

import sqlite3
import os
import hashlib
import secrets
from datetime import datetime

AUTH_DB = os.path.join(os.path.dirname(os.path.dirname(__file__)), "securevault_auth.db")


def get_connection():
    """Get a database connection with Row factory."""
    conn = sqlite3.connect(AUTH_DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_auth_db():
    """Initialize the authentication database with required tables."""
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            password_salt TEXT NOT NULL,
            email TEXT DEFAULT '',
            full_name TEXT DEFAULT '',
            role TEXT NOT NULL DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            two_fa_enabled INTEGER DEFAULT 0,
            two_fa_secret TEXT DEFAULT NULL,
            is_active INTEGER DEFAULT 1,
            avatar_color TEXT DEFAULT '#00e5ff'
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS login_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT NOT NULL,
            role TEXT NOT NULL,
            login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT DEFAULT '127.0.0.1',
            status TEXT NOT NULL,
            session_duration TEXT DEFAULT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    c.execute("""
        CREATE INDEX IF NOT EXISTS idx_login_logs_time
        ON login_logs(login_time DESC)
    """)

    c.execute("""
        CREATE INDEX IF NOT EXISTS idx_login_logs_user
        ON login_logs(username)
    """)

    conn.commit()
    conn.close()


def hash_password(password: str, salt: str = None) -> tuple:
    """Hash a password with PBKDF2-HMAC-SHA256. Returns (hash, salt)."""
    if salt is None:
        salt = secrets.token_hex(32)
    pw_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        iterations=100_000
    ).hex()
    return pw_hash, salt


def seed_default_users():
    """Create default admin and user accounts if they don't exist."""
    conn = get_connection()
    c = conn.cursor()

    default_users = [
        {
            "username": "admin",
            "password": "admin123",
            "email": "admin@securevault.io",
            "full_name": "System Administrator",
            "role": "admin",
            "avatar_color": "#a855f7"
        },
        {
            "username": "john_doe",
            "password": "user123",
            "email": "john.doe@example.com",
            "full_name": "John Doe",
            "role": "user",
            "avatar_color": "#00e5ff"
        },
        {
            "username": "jane_smith",
            "password": "user456",
            "email": "jane.smith@example.com",
            "full_name": "Jane Smith",
            "role": "user",
            "avatar_color": "#ec4899"
        },
    ]

    for user in default_users:
        c.execute("SELECT id FROM users WHERE username = ?", (user["username"],))
        if c.fetchone() is None:
            pw_hash, salt = hash_password(user["password"])
            c.execute(
                """INSERT INTO users
                   (username, password_hash, password_salt, email, full_name, role, avatar_color)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (user["username"], pw_hash, salt, user["email"],
                 user["full_name"], user["role"], user["avatar_color"])
            )

    conn.commit()
    conn.close()


# ─── Query Functions ────────────────────────────────────────

def get_user(username: str, role: str = None) -> dict | None:
    """Fetch a user by username (and optionally role). Returns dict or None."""
    conn = get_connection()
    c = conn.cursor()
    if role:
        c.execute("SELECT * FROM users WHERE username = ? AND role = ?", (username, role))
    else:
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_users() -> list:
    """Fetch all users."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, username, email, full_name, role, created_at, last_login, two_fa_enabled, is_active, avatar_color FROM users ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_last_login(user_id: int):
    """Update the last_login timestamp for a user."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE users SET last_login = ? WHERE id = ?",
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id))
    conn.commit()
    conn.close()


def record_login(user_id: int, username: str, role: str, status: str, ip: str = "127.0.0.1"):
    """Record a login attempt in the login_logs table."""
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        """INSERT INTO login_logs (user_id, username, role, login_time, ip_address, status)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (user_id, username, role, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ip, status)
    )
    conn.commit()
    conn.close()


def get_login_logs(limit: int = 100) -> list:
    """Fetch recent login logs (for admin dashboard)."""
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT * FROM login_logs ORDER BY login_time DESC LIMIT ?", (limit,)
    )
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_user_login_history(username: str, limit: int = 10) -> list:
    """Fetch login history for a specific user."""
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT * FROM login_logs WHERE username = ? ORDER BY login_time DESC LIMIT ?",
        (username, limit)
    )
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_login_stats() -> dict:
    """Get aggregate login statistics for admin dashboard."""
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM users")
    total_users = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM users WHERE role = 'user'")
    total_regular = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM login_logs")
    total_logins = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM login_logs WHERE status = 'success'")
    successful = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM login_logs WHERE status = 'failed'")
    failed = c.fetchone()[0]

    c.execute("""
        SELECT COUNT(DISTINCT username) FROM login_logs
        WHERE status = 'success'
        AND login_time >= datetime('now', '-24 hours')
    """)
    active_24h = c.fetchone()[0]

    conn.close()

    return {
        "total_users": total_users,
        "total_regular_users": total_regular,
        "total_logins": total_logins,
        "successful_logins": successful,
        "failed_logins": failed,
        "active_24h": active_24h,
    }
