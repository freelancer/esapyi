from unittest import TestCase

from dm_management.app import create_app


class AppContextTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.app = create_app()
        self.client = self.app.test_client()


class DbContextTestCase(AppContextTestCase):
    pass
