from tests.conftest import BaseTestCase

from dm_management.utils.password import (
    preprocess_password,
    hash_password,
    compare_passwords,
)


short_password = '_9XcJ.Edq*'
large_password = short_password * 11


class TestPreProcessPassword(BaseTestCase):
    def test_can_run(self) -> None:
        assert preprocess_password(short_password) is not None

    def test_can_handle_large_passwords(self) -> None:
        assert preprocess_password(large_password) is not None


class TestHashPassword(BaseTestCase):
    def test_can_run(self) -> None:
        assert hash_password(short_password) is not None

    def test_returns_a_string(self) -> None:
        assert isinstance(hash_password(short_password), str)

    def test_can_handle_large_passwords(self) -> None:
        assert hash_password(large_password) is not None


class TestComparePassword(BaseTestCase):
    def test_matches_same_password(self) -> None:
        original = short_password
        hashed = hash_password(original)

        assert compare_passwords(original, hashed)

    def test_rejects_different_passwords(self) -> None:
        original = short_password
        hashed = hash_password(large_password)

        assert not compare_passwords(original, hashed)
