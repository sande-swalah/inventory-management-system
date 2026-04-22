_revoked =  set ()

def blacklist_token(jti):
    _revoked.add(jti)

def is_token_blacklisted(jti):
    return jti in _revoked
