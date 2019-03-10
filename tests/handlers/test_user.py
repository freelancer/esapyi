from tests.conftest import DbContextTestCase

from dm_management.handlers.user import create_user
from dm_management.models.user import User
from dm_management.models.db import db


class TestCreateUser(DbContextTestCase):
    def test_function_can_run(self) -> None:
        user = create_user(
            email='test@test.com',
            password='password',
        )
        assert user is not None

    def test_model_exists(self) -> None:
        user = create_user(
            email='test@test.com',
            password='password',
        )
        db.session.query(User).all()
        #  assert user.id is not None
