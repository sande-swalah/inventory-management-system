from orders_database import get_db


class OrderRepository:
    def fetch_all_orders(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM orders")
        rows = cursor.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def fetch_order(self, order_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        return self._row_to_dict(row) if row else None

    def create_order(self, data):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO orders (product_id, quantity, order_value, status, expected_delivery, created_on)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                data["product_id"],
                data["quantity"],
                data["order_value"],
                data.get("status", "pending"),
                data.get("expected_delivery"),
                data["created_on"],
            ),
        )
        db.commit()
        return self.fetch_order(cursor.lastrowid)

    def _row_to_dict(self, row):
        return {
            "id": row["id"],
            "product_id": row["product_id"],
            "quantity": row["quantity"],
            "order_value": row["order_value"],
            "status": row["status"],
            "expected_delivery": row["expected_delivery"],
            "created_on": row["created_on"],
        }
