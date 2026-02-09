from werkzeug.security import generate_password_hash, check_password_hash


# Hash password during registration
def hash_password(password):
    return generate_password_hash(password)


# Verify password during login
def verify_password(hashed_password, password):
    return check_password_hash(hashed_password, password)
