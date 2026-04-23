from user_handling.utilities.tokens.blcklist import blacklist_token

from ...models.user_repo.user_repository import UserRepository
from ...models.user_schema.user_schema import UserSchema    
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import ValidationError, EXCLUDE
from ....utilities.tokens.jwt import generate_token, decode_token



user_schema = UserSchema()

class UserAuthService:

    def __init__(self):
        self.repo = UserRepository()

    def register(self, user_data):

        if self.repo.fetch_user_by_email(user_data.get("email")):
            return {"error": "Email already exists"}, 400
        
        try:
            create_user = user_schema.load(user_data, unknown=EXCLUDE)
        except ValidationError as err:
            return {"error": err.messages}, 422
        
        create_user.set_password(user_data.get("password"))
        self.repo.register_user(create_user)

        token = generate_token(
            user_id=create_user.id,
            roles=create_user.roles
        )
        return {"user": user_schema.dump(create_user), "token": token}, 201


    def login(self, data):

        user = self.repo.fetch_user_by_email(data.get("email"))

        if not user or not user.check_password(data.get("password")):
            return {"error": "Invalid email or password"}, 401

        token = generate_token(
            user_id=user.id,
            roles=user.roles
        )
        return {"user": user_schema.dump(user), "token": token}, 200


    def logout(self, token):

        try:
            payload = decode_token(token)
        except Exception as e:
            return {"error": str(e)}, 401

        jti = payload.get("jti")
        if not jti:
            return {"error": "Token has no jti claim"}, 400

        blacklist_token(jti)
        return {"message": "Successfully logged out"}, 200