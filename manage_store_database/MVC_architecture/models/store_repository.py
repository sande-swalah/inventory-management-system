from manage_store_database import get_db


class StoreRepository:
    def fetch_all_stores(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM stores")
        rows = cursor.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def create_store(self, store):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO stores (name, address, contact_number, email, created_on)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                store["name"],
                store["address"],
                store.get("contact_number"),
                store.get("email"),
                store["created_on"],
            ),
        )
        db.commit()
        return self.fetch_store(cursor.lastrowid)

    def fetch_store(self, store_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM stores WHERE id = ?", (store_id,))
        row = cursor.fetchone()
        return self._row_to_dict(row) if row else None

    def _row_to_dict(self, row):
        return {
            "id": row["id"],
            "name": row["name"],
            "address": row["address"],
            "contact_number": row["contact_number"],
            "email": row["email"],
            "created_on": row["created_on"],
        }
