
import json
from user_handling.user_database import get_db


class UserRepository:
    def register_user(self, user):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO users (first_name, last_name, email, password, is_active, is_deleted, roles, created_on)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user.first_name,
                user.last_name,
                user.email,
                user.password,
                int(user.is_active),
                int(user.is_deleted),
                json.dumps(user.roles),
                user.created_on.isoformat() if hasattr(user.created_on, "isoformat") else user.created_on,
            ),
        )
        user.id = cursor.lastrowid
        conn.commit()
        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": user.password,
            "is_active": user.is_active,
            "is_deleted": user.is_deleted,
            "roles": user.roles,
            "created_on": user.created_on.isoformat() if hasattr(user.created_on, "isoformat") else user.created_on,
        }

    def fetch_a_single_user(self, user_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ? AND is_deleted = 0", (user_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return self._row_to_dict(row)

    def fetch_user_by_email(self, email):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND is_deleted = 0", (email,))
        row = cursor.fetchone()
        if not row:
            return None
        return self._row_to_dict(row)

    def fetch_all_users(self):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE is_deleted = 0")
        rows = cursor.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def update_a_user(self, user_id, updated_user):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE users
            SET first_name = ?, last_name = ?, email = ?, password = ?, is_active = ?, is_deleted = ?, roles = ?, created_on = ?
            WHERE id = ?
            """,
            (
                updated_user.first_name,
                updated_user.last_name,
                updated_user.email,
                updated_user.password,
                int(updated_user.is_active),
                int(updated_user.is_deleted),
                json.dumps(updated_user.roles),
                updated_user.created_on.isoformat() if hasattr(updated_user.created_on, "isoformat") else updated_user.created_on,
                user_id,
            ),
        )
        conn.commit()
        if cursor.rowcount == 0:
            return None
        return self.fetch_a_single_user(user_id)

    def delete_a_user(self, user_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET is_deleted = 1 WHERE id = ?", (user_id,))
        conn.commit()
        return cursor.rowcount > 0

    def restore_deleted_user(self, user_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET is_deleted = 0 WHERE id = ?", (user_id,))
        conn.commit()
        return cursor.rowcount > 0

    def _row_to_dict(self, row):
        return {
            "id": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "email": row[3],
            "password": row[4],
            "is_active": bool(row[5]),
            "is_deleted": bool(row[6]),
            "roles": json.loads(row[7]) if row[7] else [],
            "created_on": row[8],
        }

  