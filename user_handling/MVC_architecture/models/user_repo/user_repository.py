from extensions import db
from marshmallow import ValidationError

from user_handling.MVC_architecture.models.user_domain.user_domain import User_Data
from user_handling.MVC_architecture.models.user_schema.user_schema import UserSchema


user_schema = UserSchema()
list_user_schema = UserSchema(many=True)


class UserRepository:

    def register_user(self, user_data):
        user = User_Data(**user_data)
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user)

    def login_user(self, email, password):
        user = User_Data.query.filter_by(email=email, is_deleted=False).first()
        if user and user.password == password:
            return user_schema.dump(user)
        return None

    def fetch_a_single_user(self, user_id):
        user = db.session.get(User_Data,(user_id))
        if not user or user.is_deleted:
            return None
        return user_schema.dump(user)

    def fetch_user_by_email(self, email):
        user = User_Data.query.filter_by(email=email, is_deleted=False).first()
        return user_schema.dump(user) if user else None

    def fetch_all_users(self):
        users = User_Data.query.order_by(User_Data.id.asc()).all()
        return list_user_schema.dump(users)

    def update_a_user(self, user_id, updated_user):
        user = db.session.get(User_Data,(user_id))
        if not user:
            return None

        for field, value in updated_user.items():
            setattr(user, field, value)

        db.session.commit()
        return user_schema.dump(user)

    def delete_a_user(self, user_id):
        user = db.session.get(User_Data,(user_id))
        if not user:
            return False

        user.is_deleted = True
        user.is_active = False
        db.session.commit()
        return True

    def restore_deleted_user(self, user_id):
        user = db.session.get(User_Data,(user_id))
        if not user:
            return False

        user.is_deleted = False
        user.is_active = True
        db.session.commit()
        return True

   