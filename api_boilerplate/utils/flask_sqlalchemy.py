from typing import Optional, Union, Any
from flask import Flask, has_request_context, has_app_context
from flask.globals import _app_ctx_stack, g as flask_g
from sqlalchemy import create_engine
from sqlalchemy.pool import Pool
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

class SqlAlchemy:
    '''
    This class is a replacement for Flask-SqlAlchemy
    It is heavily inspired by the work done by Chris Trotman from Escrow.com

    Problems with Flask-SqlAlchemy:
    - Forces you to use a connection pool with MySQL. This can't be disabled,
      and you have to work around it by monkey patching the internals.
    - It intermingles the models with the connection setup, and tries to handle
      multiple database binds, but somehow fails spectacularly and makes it
      more complicated than required.
    - It assumes you're manually committing or rolling back, and you have to
      explicitly turn on commiting or rolling back at the end of a request.

    This simple library fixes these issues by providing a much simpler
    interface for managing your SqlAlchemy connections.


    Usage as a Flask extension:
    ```
        from flask import Flask
        from api_boilerplate.utils.flask_sqlalchemy import SqlAlchemy

        db = SqlAlchemy()
        app = Flask(__name__)
        app.config['SQLALCHEMY_URI'] = 'sqlite:///temp/db.sqlite'

        db.init_app(app, 'SQLALCHEMY_URI')

        @app.route('/')
        def index():
            return db.session.execute('hello').all()
    ```

    Usage as a context manager:
    ```
        from api_boilerplate.utils.flask_sqlalchemy import SqlAlchemy

        db = SqlAlchemy(connection_string='sqlite:///temp/db.sqlite')
        with db as session:
            rows = session.execute('SELECT * from User').all()
    ```

    Usage without a context manger:
    ```
        from api_boilerplate.utils.flask_sqlalchemy import SqlAlchemy

        db = SqlAlchemy(connection_string='sqlite:///temp/db.sqlite')

        try:
            db.session.execute('SELECT * from User')
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()
            db.session.close()
    ```
    '''
    override_pool_class: Optional[Pool]
    engine: Engine
    SessionMaker: Session
    flask_context_key: str
    flask_managed_context: bool = False
    connection_string: Optional[str]
    _db: Optional[Session] = None

    def __init__(
            self,
            pool_class: Optional[Pool] = None,
            connection_string: Optional[str] = None,
    ) -> None:
        self.override_pool_class = pool_class
        self.SessionMaker = sessionmaker()  # pylint: disable=invalid-name
        self.flask_context_key = f'sqlalchemy.{id(self)}'
        self.connection_string = connection_string

        if self.connection_string:
            self.configure()

    def configure(self) -> None:
        assert self.connection_string is not None
        if self.override_pool_class:
            self.engine = create_engine(
                self.connection_string,
                pool_class=self.override_pool_class,
            )
        else:
            self.engine = create_engine(self.connection_string)

        self.SessionMaker.configure(bind=self.engine)

    def init_app(self, app: Flask, config_connection_key: str) -> None:
        self.connection_string = app.config[config_connection_key]
        self.configure()
        self.flask_managed_context = True
        app.teardown_appcontext(self.handle_teardown)
        app.teardown_request(self.handle_teardown)

    @property
    def session(self) -> Session:
        return self.get_or_create_session()

    def __enter__(self) -> Session:
        return self.session

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self.handle_teardown(error_or_code=exc_value)

    def get_or_create_session(self) -> Session:
        session = self.get_session()
        if not session:
            return self.create_session()
        return session

    def get_session(self) -> Optional[Session]:
        if self.flask_managed_context:
            ctx = self.get_flask_context()
            return getattr(ctx, self.flask_context_key, None)
        return self._db

    def create_session(self) -> Session:
        session = self.SessionMaker(bind=self.engine)
        if self.flask_managed_context:
            ctx = self.get_flask_context()
            setattr(ctx, self.flask_context_key, session)
        else:
            self._db = session
        return session

    def shutdown_session(self, rollback: bool) -> None:
        session = self.get_session()
        if session:
            if rollback or not session.is_active:
                session.rollback()
            else:
                session.commit()

            session.expunge_all()
            session.close()

    @staticmethod
    def get_flask_context() -> object:
        if has_request_context():
            return flask_g
        if has_app_context():
            return _app_ctx_stack.top
        raise Exception('Not inside flask context')

    def handle_teardown(
            self,
            error_or_code: Optional[Union[int, Exception]],
    ) -> None:
        self.shutdown_session(
            rollback=(error_or_code is not None),
        )
