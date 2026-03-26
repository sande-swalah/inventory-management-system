
class UserRepository:
    def __init__(self):
        self._store = {}
        self._deleted_user = {}
        self._email_index = {}

    def register_user(self, user):
        user_id = len(self._store) + 1
        user.id = user_id
        self._store[user_id] = user
        self._email_index[user.email] = user_id
        return user

    def fetch_a_single_user(self, user_id):
        user = self._store.get(user_id)
        if user:
            return user.to_dict()
        
        

    def fetch_all_users(self):
        return list(self._store.values())
    
    def update_a_user(self, user_id, updated_user):
        if user_id in self._store:
            self._store[user_id] = updated_user
            self._email_index[updated_user.email] = user_id
            return updated_user
        
       
    
    def delete_a_user(self, user_id):
        if user_id in self._store:
            deleted_user = self._store.pop(user_id)
            self._deleted_user[user_id] = deleted_user
            if deleted_user.email in self._email_index:
                del self._email_index[deleted_user.email]

       

    def restore_deleted_user(self, user_id):
        if user_id in self._deleted_user:
            user = self._deleted_user.pop(user_id)
            self._store[user_id] = user
            self._email_index[user.email] = user_id
            return user
   

    def has_role_access(self, user_id, allowed_roles):
        user = self._store.get(user_id)
        
        if isinstance(allowed_roles, str):
            allowed = {allowed_roles.strip().lower()}
        else:
            allowed = {str(role).strip().lower() for role in allowed_roles}

        user_roles = user.roles if isinstance(user.roles, list) else [user.roles]
        return any(str(role).strip().lower() in allowed for role in user_roles)