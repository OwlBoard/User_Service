# src/security.py
"""
DEPRECATED: This file is kept for backward compatibility only.
Authentication is now handled by the centralized Auth_Service.

For new code, use the Auth_Service endpoints:
- POST /auth/login - for authentication
- POST /auth/token/validate - for token validation

For protecting routes, use the JWT middleware:
from src.middleware.jwt_middleware import require_auth
"""

from passlib.context import CryptContext

# Password hashing context (still used for user registration)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash password using bcrypt (for user registration)"""
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """Verify password (still used for local validation)"""
    try:
        return pwd_context.verify(plain, hashed)
    except Exception:
        # Fallback for old unhashed passwords (migration period)
        return plain == hashed

def create_access_token(data: dict) -> str:
    """
    DEPRECATED: Use Auth_Service /auth/login endpoint instead
    This function is kept for backward compatibility only.
    """
    import warnings
    warnings.warn(
        "create_access_token is deprecated. Use Auth_Service /auth/login endpoint.",
        DeprecationWarning,
        stacklevel=2
    )
    return f"TOKEN-{data['sub']}"
