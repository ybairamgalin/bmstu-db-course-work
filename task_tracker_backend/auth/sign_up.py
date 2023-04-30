import random
import string
import hashlib

from task_tracker_backend import models

HASH_ALGORITHM = 'sha256'
HASH_ITERATIONS = 10_000
SALT_LENGTH = 10


def generate_salt():
    return ''.join(
        random.choice(string.ascii_letters) for _ in range(SALT_LENGTH)
    )


def hash_password_with_salt(password, salt):
    return hashlib.pbkdf2_hmac(
        HASH_ALGORITHM, password.encode(), salt.encode(), HASH_ITERATIONS
    ).hex()


def map_request_user_to_db_user(request_user: models.UserCreatePostRequest):
    salt = generate_salt()
    salted_password = hash_password_with_salt(request_user.hashed_password, salt)
    return models.DbUser(
        username=request_user.username,
        name=request_user.name,
        salted_password=salted_password,
        salt=salt,
    )
