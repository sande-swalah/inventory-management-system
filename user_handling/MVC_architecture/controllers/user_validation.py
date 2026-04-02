
def validate_email(email):
    if not email:
        return False, "Email is required"
    return True

   
def validate_password(password):
    if not password:
        return False, "Password is required"

    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    return True


