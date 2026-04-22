import os

import hashlib
import hmac


def hash_password(plain:str):

    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac(
        hashname = 'sha256',
        password= plain.encode(),
        salt= salt,
        iterations=100000)
    
    return f"{salt.hex()}:{digest.hex()}"

def verify_password(stored_password:str, provided_password:str):
    try:
       salt_hex, digest_hex = stored_password.split("$",1)
       salt = bytes.fromhex(salt_hex)
       expected = bytes.fromhex(digest_hex)

    except ValueError:
        return False