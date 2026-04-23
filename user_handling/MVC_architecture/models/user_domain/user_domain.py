from datetime import datetime
from user_handling.utilities.password_hashing.passwordhashing import hash_password, verify_password
from extensions.extensions import db
from .user_roles import UserRoles


class User_Data(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    roles = db.Column(
        db.Enum(
            UserRoles,
            native_enum=False,
            validate_strings=True,
            name="user_roles",
        ),
        nullable=False,
        default=UserRoles.GUEST,
    )
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


#relationships
    orders = db.relationship("Order_Data", back_populates="user")
    reports = db.relationship("Report_Data", back_populates="generated_for_user")
    supplier_profile = db.relationship(
        "Supplier_Data",
        back_populates="user",
        primaryjoin="User_Data.email == Supplier_Data.user_email",
        foreign_keys="Supplier_Data.user_email",
    )
    


    def set_password(self, password):
        self.password = hash_password(password)

    def check_password(self, password):
        return verify_password(self.password, password)

    

