from datetime import datetime
from ..models.user_domain import User


class UserService:

    roles = {"user", "manager", "staff"}

    def __init__(self, repo):
        self.repo = repo

    def get_all_users(self):
        users_list = self.repo.fetch_all_users()
        return [user.to_dict() for user in users_list]

    def get_user(self, user_id):
        return self.repo.fetch_a_single_user(user_id)

    def delete(self, user_id):
        return self.repo.delete_a_user(user_id)

    def restore(self, user_id):
        user = self.repo.restore_deleted_user(user_id)
        if user:
            return user.to_dict()
        

    def register(self, data):
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        password = data.get("password")
        roles = self._assign_roles_on_register(data)

        user = User(
            id=None,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_active=True,
            is_deleted=False,
            roles=roles,
            created_on=datetime.now(),
        )
        stored_user = self.repo.register_user(user)
        return stored_user.to_dict()

    def _assign_roles_on_register(self, data):
        incoming = data.get("roles")

        if incoming is None:
            return ["user"]
        
        return [role for role in incoming if role in self.roles]

    def update(self, user_id, data):
        existing = self.repo.fetch_a_single_user(user_id)
        
        updated_user = User(
            id=user_id,
            first_name=data.get("first_name", existing["first_name"]),
            last_name=data.get("last_name", existing["last_name"]),
            email=data.get("email", existing["email"]),
            password=data.get("password", existing["password"]),
            is_active=data.get("is_active", existing["is_active"]),
            is_deleted=data.get("is_deleted", existing["is_deleted"]),
            roles=data.get("roles", existing["roles"]),
            created_on=existing["created_on"],
        )
        result = self.repo.update_a_user(user_id, updated_user)
        if result:
            return result.to_dict()
        return None

    def login(self, data):
        email = data.get("email")
        password = data.get("password")


        user = self.repo.fetch_user_by_email(email)
        

        return user.to_dict()

    def has_role_access(self, user_id, allowed_roles):
        return self.repo.has_role_access(user_id, allowed_roles)
