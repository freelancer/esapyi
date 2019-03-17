import os
from unittest import TestCase
from alembic import command as alembic_command
from alembic.config import Config as AlembicConfig

from dm_management.app import create_app
from dm_management.utils.db import wait_for_db


class AppContextTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.app = create_app()
        self.client = self.app.test_client()


class DbContextTestCase(AppContextTestCase):
    def setUp(self) -> None:
        super().setUp()

        # wait for a db connection and then run upgrade
        wait_for_db(
            db_tcp_addr=os.environ['DM_MANAGEMENT_DB_PORT_3306_TCP_ADDR'],
            db_tcp_port=int(os.environ['DM_MANAGEMENT_DB_PORT_3306_TCP_PORT']),
        )

        # ensure all tables are created
        with self.app.app_context():
            alembic_config = AlembicConfig('alembic.ini')
            alembic_command.downgrade(alembic_config, 'base')
            alembic_command.upgrade(alembic_config, 'head')