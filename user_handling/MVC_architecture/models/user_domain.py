
class User:

    def __init__(self, id, first_name, last_name, email, password, is_active, is_deleted, roles, created_on):

        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_active = is_active
        self.is_deleted = is_deleted
        self.roles = roles
        self.created_on = created_on

   
    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "roles": self.roles,
            "is_active": self.is_active,
            "is_deleted": self.is_deleted,
            "created_on": self.created_on
        }
