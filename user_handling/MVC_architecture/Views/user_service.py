from datetime import datetime
from ..models.user_domain.user_domain import User_Data
from ..models.user_domain.user_roles import UserRoles


ROLE_MAP = {
    "user": UserRoles.USER,
    "staff": UserRoles.STAFF,
    "manager": UserRoles.MANAGER,
    "admin": UserRoles.ADMIN,
    "supplier": UserRoles.SUPPLIER,
    "guest": UserRoles.GUEST,
}


class UserService:

    def __init__(self, repo):
        self.repo = repo

    def get_all_users(self):
        return self.repo.fetch_all_users()

    def get_user(self, user_id):
        return self.repo.fetch_a_single_user(user_id)

    def delete(self, user_id):
        return self.repo.delete_a_user(user_id)

    def restore(self, user_id):
        return self.repo.restore_deleted_user(user_id)

    def register(self, data):
        roles = self._assign_roles_on_register(data)

        user = {
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "email": data.get("email"),
            "password": data.get("password"),
            "is_active": True,
            "is_deleted": False,
            "roles": roles,
            "created_on": datetime.utcnow(),
        }
        return self.repo.register_user(user)

    def _assign_roles_on_register(self, data):
        incoming = data.get("roles")

        if incoming is None:
            return UserRoles.USER

        if isinstance(incoming, str):
            return ROLE_MAP.get(incoming.lower(), UserRoles.USER)

        if not isinstance(incoming, list):
            return UserRoles.USER
        
        for role in incoming:
            if isinstance(role, str) and role.lower() in ROLE_MAP:
                return ROLE_MAP[role.lower()]

        return UserRoles.USER

    def update(self, user_id, data):
        existing = self.repo.fetch_a_single_user(user_id)
        if not existing:
            return None

        role_value = existing["roles"]
        if "roles" in data:
            role_value = self._assign_roles_on_register({"roles": data.get("roles")})
        
        updated_user = {
            "first_name": data.get("first_name", existing["first_name"]),
            "last_name": data.get("last_name", existing["last_name"]),
            "email": data.get("email", existing["email"]),
            "password": data.get("password", existing.get("password")),
            "is_active": data.get("is_active", existing["is_active"]),
            "is_deleted": data.get("is_deleted", existing["is_deleted"]),
            "roles": role_value,
        }
        return self.repo.update_a_user(user_id, updated_user)

    def login(self, data):
        email = data.get("email")
        password = data.get("password")

        user = self.repo.fetch_user_by_email(email)
        if not user:
            return None

        if user.get("password") != password:
            return None

        return user

    def check_user_roles(self, user_id, required_roles):
        user = self.get_user(user_id)
        if not user:
            return False
        
        user_role = user.get("roles")
        if user_role is None:
            return False

        user_role_text = str(user_role).lower()
        if "." in user_role_text:
            user_role_text = user_role_text.split(".")[-1]

        return user_role_text in {role.lower() for role in required_roles}

    