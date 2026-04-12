from products_database import get_db


class ProductRepository:
    def fetch_all_products(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def fetch_product(self, product_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        return self._row_to_dict(row) if row else None

    def create_product(self, data):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO products (name, category, buying_price, quantity, threshold, expiry_date, supplier_id, created_on)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["name"],
                data.get("category"),
                data.get("buying_price", 0),
                data.get("quantity", 0),
                data.get("threshold", 0),
                data.get("expiry_date"),
                data.get("supplier_id"),
                data["created_on"],
            ),
        )
        db.commit()
        return self.fetch_product(cursor.lastrowid)

    def update_product(self, product_id, data):
        existing = self.fetch_product(product_id)
        if not existing:
            return None
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """
            UPDATE products
            SET name = ?, category = ?, buying_price = ?, quantity = ?, threshold = ?, expiry_date = ?, supplier_id = ?
            WHERE id = ?
            """,
            (
                data.get("name", existing["name"]),
                data.get("category", existing["category"]),
                data.get("buying_price", existing["buying_price"]),
                data.get("quantity", existing["quantity"]),
                data.get("threshold", existing["threshold"]),
                data.get("expiry_date", existing["expiry_date"]),
                data.get("supplier_id", existing["supplier_id"]),
                product_id,
            ),
        )
        db.commit()
        return self.fetch_product(product_id)

    def delete_product(self, product_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        db.commit()
        return cursor.rowcount > 0

    def _row_to_dict(self, row):
        return {
            "id": row["id"],
            "name": row["name"],
            "category": row["category"],
            "buying_price": row["buying_price"],
            "quantity": row["quantity"],
            "threshold": row["threshold"],
            "expiry_date": row["expiry_date"],
            "supplier_id": row["supplier_id"],
            "created_on": row["created_on"],
        }
