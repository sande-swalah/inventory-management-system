from datetime import datetime
from ..models.user_domain.user_domain import User_Data
from ..models.user_domain.user_roles import UserRoles
from user_handling.utilities.password_hashing.passwordhashing import hash_password, verify_password
from user_handling.utilities.tokens.jwt import generate_token


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
        if self.repo.fetch_user_by_email(data.get("email")):
            return {"error": "Email already exists"}, 400

        roles = self._assign_roles_on_register(data)

        user = {
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "email": data.get("email"),
            "password": hash_password(data.get("password")),
            "is_active": True,
            "is_deleted": False,
            "roles": roles,
            "created_on": datetime.utcnow(),
        }
        created_user = self.repo.register_user(user)
        token = generate_token(
            user_id=created_user["id"],
            roles=created_user["roles"]
        )
        return {"user": created_user, "token": token}

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

        if not data:
            raise ValueError("No update data provided")

        allowed_fields = {
            "first_name",
            "last_name",
            "email",
            "password",
            "is_active",
            "is_deleted",
            "roles",
        }

        for field in data:
            if field not in allowed_fields:
                raise ValueError(f"Unknown field: {field}")

        updated_user = {}

        if "first_name" in data:
            updated_user["first_name"] = data.get("first_name")
        if "last_name" in data:
            updated_user["last_name"] = data.get("last_name")
        if "email" in data:
            updated_user["email"] = data.get("email")
        if "is_active" in data:
            updated_user["is_active"] = data.get("is_active")
        if "is_deleted" in data:
            updated_user["is_deleted"] = data.get("is_deleted")
        if "roles" in data:
            updated_user["roles"] = self._assign_roles_on_register({"roles": data.get("roles")})

        # Preserve current password hash unless a new password is explicitly provided.
        if "password" in data:
            raw_password = data.get("password")
            if not raw_password:
                raise ValueError("Password cannot be empty")
            updated_user["password"] = hash_password(raw_password)

        return self.repo.update_a_user(user_id, updated_user)

    def login(self, data):
        email = data.get("email")
        password = data.get("password")

        user_obj = self.repo.fetch_user_for_auth(email)
        if not user_obj:
            return None

        if not verify_password(user_obj.password, password):
            return None

        from ..models.user_schema.user_schema import UserSchema
        user_dict = UserSchema().dump(user_obj)
        roles_value = user_obj.roles.value if hasattr(user_obj.roles, "value") else str(user_obj.roles)
        token = generate_token(
            user_id=user_obj.id,
            roles=roles_value
        )
        return {"user": user_dict, "token": token}

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

    