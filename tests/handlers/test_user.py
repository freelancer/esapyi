from tests.conftest import DbContextTestCase

from dm_management.handlers.user import create_user
from dm_management.models.user import User
from dm_management.models.db import db


class TestCreateUser(DbContextTestCase):
    def test_returned_user_has_id(self) -> None:
        with self.app.app_context():
            user = create_user(
                email='test@test.com',
                password='password',
            )
            assert user is not None
            assert user.id is not None

    def test_created_user_is_queryable(self) -> None:
        with self.app.app_context():
            user = create_user(
                email='test@test.com',
                password='password',
            )
            user_id = user.id

        with self.app.app_context():
            queried_user = db.session.query(User).filter(
                User.id == user_id,
            ).first()

            assert queried_user is not None
