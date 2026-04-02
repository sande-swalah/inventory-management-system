import sqlite3
from flask import g

DATABASE = "users.db"


def get_db():
    """Return an SQLite connection from Flask context."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e):
    """Close the database connection"""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Initialize the database schema."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT 1,
            is_deleted BOOLEAN NOT NULL DEFAULT 0,
            roles TEXT NOT NULL DEFAULT 'user',
            created_on TEXT NOT NULL
        );
        """
    )
    conn.commit()
    cursor.close()
    conn.close()


def init_app(app):
    """Register teardown callback for application."""
    app.teardown_appcontext(close_db)


    