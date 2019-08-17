from unittest.mock import patch, MagicMock

from tests.conftest import AppContextTestCase

from api_boilerplate.models.user import User
from api_boilerplate.handlers.user import (
    create_user,
    get_user_by_email,
)


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
        'api_boilerplate.v1.user.create_user',
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


class TestFilterUser(AppContextTestCase):
    def test_returns_422_when_missing_fields(self) -> None:
        response = self.client.get(
            '/v1/user',
            data={},
        )
        assert response.status_code == 422

    @patch(
        'api_boilerplate.v1.user.get_user_by_email',
        new=MagicMock(
            spec=get_user_by_email,
            return_value=user_mock,
        ),
    )
    def test_can_find_by_email(self) -> None:
        response = self.client.get(
            '/v1/user',
            data={
                'email': 'test@test.com',
            }
        )
        assert response.status_code == 200
        response_data = response.json
        assert 'users' in response_data
        assert len(response_data['users']) == 1
