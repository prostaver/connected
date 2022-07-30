import bcrypt

salt = b"$2b$12$NmAX6M5wYIW1jM8sT9bAR."

def hash_password(password: str):
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))