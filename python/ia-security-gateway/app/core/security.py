"""
Security and authentication utilities
"""
from datetime import datetime, timedelta
from typing import Optional
import jwt
from functools import wraps

SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=1)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_token(token: str) -> dict:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.InvalidTokenError:
        return None

def sanitize_input(data: str) -> str:
    """Sanitize user input to prevent injection attacks"""
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', ';', '|', '`']
    for char in dangerous_chars:
        data = data.replace(char, '')
    return data.strip()

def classify_data_sensitivity(text: str) -> str:
    """
    Classify data sensitivity level
    Returns: 'public', 'internal', 'sensitive', 'critical'
    """
    sensitive_keywords = ['password', 'token', 'key', 'secret', 'credit card']
    critical_keywords = ['ssn', 'credit card', 'passport', 'dni']

    text_lower = text.lower()

    # Check for critical data
    if any(keyword in text_lower for keyword in critical_keywords):
        return 'critical'

    # Check for sensitive data
    if any(keyword in text_lower for keyword in sensitive_keywords):
        return 'sensitive'

    # Check for internal data (email, phone, etc)
    if '@' in text or '+' in text:
        return 'internal'

    return 'public'
