import re

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_email(email):
    if not email:
        return False, "Email is required"
    if not isinstance(email) or not EMAIL_REGEX.match(email):
        return False, "Email must be a valid email address"
    return True, None


def validate_password(password):
    if not password:
        return False, "Password is required"
    if not isinstance(password, str):
        return False, "Password must be a string"
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    return True, None


def validate_name(name, field_name):
    if not name:
        return False, f"{field_name} is required"
    if not isinstance(name, str):
        return False, f"{field_name} must be a string"
    if len(name.strip()) < 2:
        return False, f"{field_name} must be at least 2 characters long"
    return True, None


def validate_roles(roles):
    if roles is None:
        return True, None
    if not isinstance(roles, list):
        return False, "Roles must be provided as a list"
    for role in roles:
        if not isinstance(role, str) or not role.strip():
            return False, "Each role must be a non-empty string"
    return True, None


def validate_registration_data(data):
    errors = []

    valid, message = validate_name(data.get("first_name"), "First name")
    if not valid:
        errors.append(message)

    valid, message = validate_name(data.get("last_name"), "Last name")
    if not valid:
        errors.append(message)

    valid, message = validate_email(data.get("email"))
    if not valid:
        errors.append(message)

    valid, message = validate_password(data.get("password"))
    if not valid:
        errors.append(message)

    valid, message = validate_roles(data.get("roles"))
    if not valid:
        errors.append(message)

    return len(errors) == 0, errors


def validate_login_data(data):
    errors = []

    valid, message = validate_email(data.get("email"))
    if not valid:
        errors.append(message)

    valid, message = validate_password(data.get("password"))
    if not valid:
        errors.append(message)

    return len(errors) == 0, errors


def validate_update_data(data):
    errors = []

    if "first_name" in data:
        valid, message = validate_name(data.get("first_name"), "First name")
        if not valid:
            errors.append(message)

    if "last_name" in data:
        valid, message = validate_name(data.get("last_name"), "Last name")
        if not valid:
            errors.append(message)

    if "email" in data:
        valid, message = validate_email(data.get("email"))
        if not valid:
            errors.append(message)

    if "password" in data:
        valid, message = validate_password(data.get("password"))
        if not valid:
            errors.append(message)

    if "roles" in data:
        valid, message = validate_roles(data.get("roles"))
        if not valid:
            errors.append(message)

    return len(errors) == 0, errors