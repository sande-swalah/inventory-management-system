from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

from user_handling.MVC_architecture.models.user_domain.user_domain import User_Data


class UserSchema(SQLAlchemyAutoSchema):
    roles = fields.Method("get_roles")

    def get_roles(self, obj):
        role = getattr(obj, "roles", None)
        if role is None:
            return None
        return role.value if hasattr(role, "value") else str(role)

    class Meta:
        model = User_Data
        load_instance = True
        exclude = ("password",)


