from datetime import datetime
from user_handling.utilities.password_hashing.passwordhashing import hash_password, verify_password
from extensions.extensions import db
from .user_roles import UserRoles


class User_Data(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(255))
    is_active = db.Column(db.Boolean)
    is_deleted = db.Column(db.Boolean)
    roles = db.Column(
        db.Enum(
            UserRoles,
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
            native_enum=False,
            validate_strings=True,
            name="user_roles",
        ),
        nullable=False,
        default=UserRoles.USER,
    )
    created_on = db.Column(db.DateTime, default=datetime.utcnow)


    def set_password(self, password):
        self.password = hash_password(password)

    def check_password(self, password):
        return verify_password(self.password, password)

    

