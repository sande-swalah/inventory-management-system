import enum


class UserRoles(enum.Enum):
    USER = "user"
    MANAGER = "manager"
    STAFF = "staff"
    SUPPLIER = "supplier"
    ADMIN = "admin"
    GUEST = "guest"
    