from unittest.mock import patch, MagicMock
import pytest
from flask import Flask

from tests.conftest import AppContextTestCase, DbContextTestCase
from dm_management.utils.flask_sqlalchemy import SqlAlchemy as FlaskSqlAlchemy
from dm_management.models.user import User


class TestBasicMethods(AppContextTestCase):
    @patch.object(FlaskSqlAlchemy, 'get_session')
    def test_shutdown_session_rollback(
            self,
            get_session_mock: MagicMock,
    ) -> None:
        session_mock = MagicMock()
        session_mock.is_active = True
        get_session_mock.return_value = session_mock
        db = FlaskSqlAlchemy()

        # test rollback = True
        db.shutdown_session(rollback=True)
        session_mock.rollback.assert_called_once()
        session_mock.commit.assert_not_called()

        # test rollback = False
        session_mock.reset_mock(return_value=True, side_effect=True)
        db.shutdown_session(rollback=False)
        session_mock.rollback.assert_not_called()
        session_mock.commit.assert_called_once()

    def test_in_flask_context(self) -> None:
        with self.app.app_context():
            FlaskSqlAlchemy.get_flask_context()

    def test_out_of_flask_context(self) -> None:
        with pytest.raises(Exception):
            FlaskSqlAlchemy.get_flask_context()

    @patch.object(FlaskSqlAlchemy, 'shutdown_session')
    def test_handle_teardown(self, shutdown_session_mock: MagicMock) -> None:
        db = FlaskSqlAlchemy()

        # test with exception
        db.handle_teardown(Exception())
        shutdown_session_mock.assert_called_once_with(rollback=True)

        # test without exception
        shutdown_session_mock.reset_mock()
        db.handle_teardown(None)
        shutdown_session_mock.assert_called_once_with(rollback=False)


class TestFlaskHooks(DbContextTestCase):
    def setUp(self) -> None:
        super().setUp()

        # setup a fresh flask application
        self.fresh_app = Flask(__name__)
        self.fresh_app.config['SQLALCHEMY_DB_URI'] = self.app.config[
            'SQLALCHEMY_DB_URI'
        ]
        self.fresh_client = self.fresh_app.test_client()

        # create a fresh instance of FlaskSqlAlchemy
        self.fresh_db = FlaskSqlAlchemy()
        self.fresh_db.init_app(
            app=self.fresh_app,
            config_connection_key='SQLALCHEMY_DB_URI',
        )

        # setup good and bad routes
        self.fresh_app.add_url_rule('/good', 'good', self.good_route)
        self.fresh_app.add_url_rule('/bad', 'bad', self.bad_route)

    def good_route(self) -> str:
        self.fresh_db.session.execute(
            '''
            INSERT INTO user (email, password)
            VALUES ('good@test.com', '123')
            '''
        )
        return 'Hello world'

    def bad_route(self) -> str:
        self.fresh_db.session.execute(
            '''
            INSERT INTO user (email, password)
            VALUES ('bad@test.com', '123')
            '''
        )
        raise Exception()

    def test_good_route(self) -> None:
        with self.fresh_app.app_context():
            response = self.fresh_client.get('/good')
            assert response.status_code == 200

            # check that data has been inserted into the db
            user = self.fresh_db.session.query(User).filter_by(
                email='good@test.com',
            ).first()
            assert user is not None

    def test_bad_route(self) -> None:
        # check that the db rolled back
        with self.fresh_app.app_context():
            response = self.fresh_client.get('/bad')
            assert response.status_code == 500

            # check that the db rolled back
            user = self.fresh_db.session.query(User).filter_by(
                email='bad@test.com',
            ).first()
            assert user is None
