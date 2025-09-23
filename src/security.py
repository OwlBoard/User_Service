# src/security.py
def hash_password(password: str) -> str:
    return password  # sin hash, directo

def verify_password(plain: str, hashed: str) -> bool:
    return plain == hashed

def create_access_token(data: dict) -> str:
    # token falso, simplemente devuelves el email o id
    return f"TOKEN-{data['sub']}"
