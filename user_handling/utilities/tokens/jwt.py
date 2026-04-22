import base64
import json
import hmac
import hashlib
import uuid
from datetime import datetime, timezone


from flask import current_app

def secret_key():
    return current_app.config.get("SECRET_KEY", "default_secret_key")


def _expiry_time():
    expiration_seconds = current_app.config.get("TOKEN_EXPIRATION_SECONDS", 3600)
    return datetime.now(timezone.utc).timestamp() + expiration_seconds

def _b64url_encode(bytes):
    pad =  4 - (len(bytes) % 4)
    if pad != 4:
        bytes += b'=' * pad
    return base64.urlsafe_b64encode(bytes)


def _sign(message):

    raw = hmac.new(secret_key().encode(), 
                   message.encode(), 
                   hashlib.sha256
                   ).digest()
    return _b64url_encode(raw).decode()

def generate_token(user_id, roles):
    now = int(datetime.now(timezone.utc).timestamp())
    header = _b64url_encode(
        json.dumps({
        "alg": "HS256",
          "typ": "JWT"
          }, separators=(",", ":")).encode()
    )
    
    payload =_b64url_encode(
        json.dumps({
        "sub": user_id,
        "roles": roles,
        "iat": now,
        "exp": now + _expiry_time(),
        "jti": str(uuid.uuid4())
        }, separators=(",", ":")).encode()
    )
    
    return f"{header}.{payload}.{_sign(f'{header}.{payload}')}"


def decode_token(token):
    try:
        token = data.split(".")


        if len(token) != 3:
            raise ValueError("Invalid token format")

        header_b64, payload_b64, signature = token

        if not hmac.compare_digest(signature, _sign(f"{header_b64}.{payload_b64}")):
            raise ValueError("Invalid token signature")
        
        payload =  json.loads(_b64url_decode(payload_b64.encode))

        if payload.get("exp", 0) < datetime.now(timezone.utc).timestamp():
            raise ValueError("Token has expired")
        
        return payload
    
    except KeyError as err:
        raise ValueError("Token not decoded")  from err
    
    
        
