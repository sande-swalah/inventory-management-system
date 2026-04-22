from user_handling.utilities.tokens.blcklist import blacklist_token

from ...models.user_repo.user_repository import UserRepository
from ...models.user_schema.user_schema import UserSchema    
from marshmallow import ValidationError
from ....utilities.tokens.jwt import generate_token, decode_token



user_schema = UserSchema()

class UserAuthService:

    def __init__(self):
        self.repo = UserRepository()

    def register(self, user_data):

        if self.repo.fetch_user_by_email(user_data.get("email")):
            return {"error": "Email already exists"}, 400
        
        try:
            create_user = user_schema.load(user_data)
        except ValidationError as err:
            return {"error": err.messages}, 422
        
        create_user.set_password(user_data.get("password"))
        self.repo.register_user(create_user)
        self.repo.save(create_user)
        return user_schema.dump(create_user)


    def login(self, data):

        user = self.repo.fetch_user_by_email(data.get("email"))

        if not user or not user.check_password(data.get("password")):
            return {"error": "Invalid email or password"}, 401
        
        #create a token here 
        token = generate_token(
            user_id=user.id,
            roles=user.roles
        )


        try:
            validated_data = user_schema.load(data)
        except ValidationError as err:
            return {"error": err.messages}, 422
        
        email = validated_data.get("email")
        password = validated_data.get("password")
        
        user = self.repo.login_user(email, password)
        if user:
            return user_schema.dump(user)
        return {"error": "Invalid email or password"}, 401
    

    def logout(self,token):

        try:
            payload = decode_token(token)
        except Exception as e:
            return {"error": str(e)}, 401
        

        if jti := payload.get("jti"):
            return {"message": "Successfully logged out"}, 200
        
        return None