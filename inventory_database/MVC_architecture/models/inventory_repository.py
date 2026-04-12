from inventory_database import get_db


class InventoryRepository:
    def fetch_all_items(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM inventory_items")
        rows = cursor.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def fetch_item(self, item_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM inventory_items WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        return self._row_to_dict(row) if row else None

    def create_item(self, item):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO inventory_items (product_id, store_id, quantity, threshold, last_updated)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                item["product_id"],
                item["store_id"],
                item["quantity"],
                item["threshold"],
                item["last_updated"],
            ),
        )
        db.commit()
        return self.fetch_item(cursor.lastrowid)

    def update_item(self, item_id, item):
        existing = self.fetch_item(item_id)
        if not existing:
            return None
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """
            UPDATE inventory_items
            SET product_id = ?, store_id = ?, quantity = ?, threshold = ?, last_updated = ?
            WHERE id = ?
            """,
            (
                item.get("product_id", existing["product_id"]),
                item.get("store_id", existing["store_id"]),
                item.get("quantity", existing["quantity"]),
                item.get("threshold", existing["threshold"]),
                item.get("last_updated", existing["last_updated"]),
                item_id,
            ),
        )
        db.commit()
        return self.fetch_item(item_id)

    def delete_item(self, item_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM inventory_items WHERE id = ?", (item_id,))
        db.commit()
        return cursor.rowcount > 0

    def _row_to_dict(self, row):
        return {
            "id": row["id"],
            "product_id": row["product_id"],
            "store_id": row["store_id"],
            "quantity": row["quantity"],
            "threshold": row["threshold"],
            "last_updated": row["last_updated"],
        }
