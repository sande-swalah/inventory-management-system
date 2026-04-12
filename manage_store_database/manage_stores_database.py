import sqlite3
from flask import g

DATABASE = "stores.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS stores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            contact_number TEXT,
            email TEXT,
            created_on TEXT NOT NULL
        );
        """
    )
    db.commit()
    cursor.close()
    db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
