from abc import ABC, abstractmethod


class IUserRepository(ABC):

    @abstractmethod
    def register_user(self, user):
        pass

    @abstractmethod
    def fetch_a_single_user(self, user_id):
        pass

    @abstractmethod
    def fetch_all_users(self):
        pass

    @abstractmethod
    def update_a_user(self, user_id, updated_user):
        pass

    @abstractmethod
    def delete_a_user(self, user_id):
        pass

    @abstractmethod
    def restore_deleted_user(self, user_id):
        pass

    @abstractmethod
    def fetch_user_by_email(self, email):
        pass
