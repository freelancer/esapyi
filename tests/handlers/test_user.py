import pytest
from tests.conftest import DbContextTestCase

from api_boilerplate.handlers.user import (
    create_user,
    get_user_by_email,
    get_user_by_id,
)
from api_boilerplate.exceptions.user import (
    UserNotFoundException,
    UserAlreadyExistsException,
)
from api_boilerplate.models.user import User
from api_boilerplate.models.db import db


class TestCreateUser(DbContextTestCase):
    email = 'test@test.com'

    def test_returned_user_has_id(self) -> None:
        with self.app.app_context():
            user = create_user(
                email=self.email,
                password='password',
            )
            assert user is not None
            assert user.id is not None

    def test_created_user_is_queryable(self) -> None:
        with self.app.app_context():
            user = create_user(
                email=self.email,
                password='password',
            )
            user_id = user.id

        with self.app.app_context():
            queried_user = db.session.query(User).filter(
                User.id == user_id,
            ).first()

            assert queried_user is not None

    def test_fails_with_duplicate_email(self) -> None:
        with self.app.app_context():
            create_user(
                email=self.email,
                password='password',
            )
        with self.app.app_context():
            with pytest.raises(UserAlreadyExistsException):
                create_user(
                    email=self.email,
                    password='password',
                )


class TestGetUserByEmail(DbContextTestCase):
    email = 'test@test.com'

    def setUp(self) -> None:
        super().setUp()
        with self.app.app_context():
            db.session.add(User(
                email=self.email,
                password='test123',
            ))

    def test_finds_created_user(self) -> None:
        with self.app.app_context():
            user = get_user_by_email(email=self.email)
            assert user.email == self.email

    def test_raises_exception_if_not_found(self) -> None:
        with self.app.app_context():
            with pytest.raises(UserNotFoundException):
                get_user_by_email(email='nothing@nothing.com')


class TestGetUserById(DbContextTestCase):
    email = 'test@test.com'
    user_id: int

    def setUp(self) -> None:
        super().setUp()
        with self.app.app_context():
            user = create_user(
                email=self.email,
                password='test123',
            )
            self.user_id = user.id

    def test_finds_created_user(self) -> None:
        with self.app.app_context():
            user = get_user_by_id(user_id=self.user_id)
            assert user.email == self.email
            assert user.id == self.user_id

    def test_raises_exception_if_not_found(self) -> None:
        with self.app.app_context():
            with pytest.raises(UserNotFoundException):
                get_user_by_id(user_id=1234)
