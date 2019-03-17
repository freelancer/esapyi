from unittest.mock import patch, MagicMock

from tests.conftest import AppContextTestCase

from dm_management.models.user import User
from dm_management.handlers.user import create_user


user_mock = User(
    id=123,
    email='test@test.com',
    password='secret',
)


class TestCreateUser(AppContextTestCase):
    def test_returns_422_when_missing_fields(self) -> None:
        response = self.client.post(
            '/v1/user',
            data={
                'email': 'test@test.com',
            }
        )
        assert response.status_code == 422

    @patch(
        'dm_management.v1.user.create_user',
        new=MagicMock(
            spec=create_user,
            return_value=user_mock,
        ),
    )
    def test_returns_200_on_success(self) -> None:
        response = self.client.post(
            '/v1/user',
            data={
                'email': 'test@test.com',
                'password': 'pwd',
            }
        )
        assert response.status_code == 200
