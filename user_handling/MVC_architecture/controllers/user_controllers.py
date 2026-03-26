from ..models.user_repository import UserRepository
from ..services.user_service import UserService


class UserController:

    def __init__(self, user_service):
        self.service = user_service

    def get_all_users(self):
        return self.service.get_all_users()

    def get_user(self, user_id):
        return self.service.get_user(user_id)

    def register(self, data):
        return self.service.register(data)

    def login(self, data):
        return self.service.login(data)

    def update(self, user_id, data):
        return self.service.update(user_id, data)

    def delete(self, user_id):
        return self.service.delete(user_id)

    def restore(self, user_id):
        return self.service.restore(user_id)

    def has_role_access(self, user_id, allowed_roles):
        return self.service.has_role_access(user_id, allowed_roles)


user_repository = UserRepository()
user_service = UserService(user_repository)
user_controller = UserController(user_service)