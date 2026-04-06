
import json
from user_handling.user_database import get_db


class UserRepository:
    def register_user(self, user):
        db = get_db()
        cursor = db.cursor()
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
                user.is_active,
                user.is_deleted,
                json.dumps(user.roles) if isinstance(user.roles, list) else user.roles,
                user.created_on
            ),
        )
        user.id = cursor.lastrowid
        db.commit()
        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": user.password,
            "is_active": user.is_active,
            "is_deleted": user.is_deleted,
            "roles": user.roles,
            "created_on": user.created_on,
        }

    def fetch_a_single_user(self, user_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ? AND is_deleted = 0", (user_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return self._row_to_dict(row)

    def fetch_user_by_email(self, email):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND is_deleted = 0", (email,))
        row = cursor.fetchone()
        if not row:
            return None
        return self._row_to_dict(row)

    def fetch_all_users(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def update_a_user(self, user_id, updated_user):
        db = get_db()
        cursor = db.cursor()
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
                updated_user.is_active,
                updated_user.is_deleted,
                json.dumps(updated_user.roles) if isinstance(updated_user.roles, list) else updated_user.roles,
                updated_user.created_on,
                user_id,
            ),
        )
        db.commit()
        return self.fetch_a_single_user(user_id)

    def delete_a_user(self, user_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE users SET is_deleted = 1 WHERE id = ?", (user_id,))
        db.commit()
        return cursor.rowcount > 0

    def restore_deleted_user(self, user_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE users SET is_deleted = 0 WHERE id = ?", (user_id,))
        db.commit()
        return cursor.rowcount > 0

    def _row_to_dict(self, row):
        """Convert a database row to a dictionary."""
        roles_str = row["roles"]
        try:
            roles = json.loads(roles_str) if roles_str else ["user"]
        except (json.JSONDecodeError, TypeError):
            # Handle legacy data or single role strings
            roles = [roles_str] if roles_str else ["user"]
        
        
        return {
            "id": row["id"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "email": row["email"],
            "password": row["password"],
            "is_active": bool(row["is_active"]),
            "is_deleted": bool(row["is_deleted"]),
            "roles": roles,
            "created_on": row["created_on"],
        }

   