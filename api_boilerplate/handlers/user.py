from api_boilerplate.models.user import User
from api_boilerplate.models.db import db
from api_boilerplate.utils.password import hash_password
from api_boilerplate.exceptions.user import (
    UserNotFoundException,
    UserAlreadyExistsException,
)


def get_user_by_email(email: str) -> User:
    user = db.session.query(User).filter(
        User.email == email,
    ).one_or_none()

    if not user:
        raise UserNotFoundException(
            f'User with email {email} does not exist'
        )

    return user

def get_user_by_id(user_id: int) -> User:
    user = db.session.query(User).filter(
        User.id == user_id,
    ).one_or_none()

    if not user:
        raise UserNotFoundException(
            f'User with id {user_id} does not exist'
        )

    return user


def create_user(email: str, password: str) -> User:
    existing_user = None
    try:
        existing_user = get_user_by_email(email=email)
    except UserNotFoundException:
        pass

    if existing_user:
        raise UserAlreadyExistsException(
            f'User with email {email} already exists'
        )

    user = User(
        email=email,
        password=hash_password(password=password),
    )
    db.session.add(user)
    db.session.flush()
    return user
