import sqlite3
from flask import g

DATABASE = "inventory.db"


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
        CREATE TABLE IF NOT EXISTS inventory_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            store_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            threshold INTEGER NOT NULL DEFAULT 0,
            last_updated TEXT NOT NULL
        );
        """
    )
    db.commit()
    cursor.close()
    db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
