# verification.py
import secrets
from datetime import datetime, timedelta

verification_codes = {} 

def generate_code() -> str:
    return f"{secrets.randbelow(1000000):06d}"  # 6-digit

def store_code(email: str, code: str, expires_in_minutes: int = 10):
    verification_codes[email] = {
        "code": code,
        "expires": datetime.utcnow() + timedelta(minutes=expires_in_minutes)
    }

def verify_code(email: str, code: str) -> bool:
    record = verification_codes.get(email)
    if not record:
        return False
    if datetime.utcnow() > record["expires"]:
        del verification_codes[email]
        return False
    if record["code"] == code:
        del verification_codes[email]
        return True
    return False