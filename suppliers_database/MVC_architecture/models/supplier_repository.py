from suppliers_database import get_db


class SupplierRepository:
    def fetch_all_suppliers(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM suppliers")
        rows = cursor.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def fetch_supplier(self, supplier_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM suppliers WHERE id = ?", (supplier_id,))
        row = cursor.fetchone()
        return self._row_to_dict(row) if row else None

    def create_supplier(self, data):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO suppliers (name, product, category, contact_number, email, supplier_type, created_on)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["name"],
                data.get("product"),
                data.get("category"),
                data.get("contact_number"),
                data.get("email"),
                data.get("supplier_type"),
                data["created_on"],
            ),
        )
        db.commit()
        return self.fetch_supplier(cursor.lastrowid)

    def _row_to_dict(self, row):
        return {
            "id": row["id"],
            "name": row["name"],
            "product": row["product"],
            "category": row["category"],
            "contact_number": row["contact_number"],
            "email": row["email"],
            "supplier_type": row["supplier_type"],
            "created_on": row["created_on"],
        }
