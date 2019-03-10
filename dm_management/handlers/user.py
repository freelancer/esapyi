from dm_management.models.user import User
from dm_management.models.db import db
from dm_management.utils.password import hash_password


def create_user(email: str, password: str) -> User:
    user = User(
        email=email,
        password=hash_password(password=password),
    )
    db.session.add(user)
    db.session.commit()
    return user
