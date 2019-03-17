from typing import Optional, Union
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
    '''
    override_pool_class: Optional[Pool]
    engine: Engine
    SessionMaker: Session
    flask_context_key: str

    def __init__(
            self,
            pool_class: Optional[Pool] = None
    ) -> None:
        self.override_pool_class = pool_class
        self.SessionMaker = sessionmaker()  # pylint: disable=invalid-name
        self.flask_context_key = f'sqlalchemy.{id(self)}'

    def init_app(self, app: Flask, config_connection_key: str) -> None:
        if self.override_pool_class:
            self.engine = create_engine(
                app.config[config_connection_key],
                pool_class=self.override_pool_class,
            )
        else:
            self.engine = create_engine(app.config[config_connection_key])

        self.SessionMaker.configure(bind=self.engine)
        app.teardown_appcontext(self.handle_teardown)

    @property
    def session(self) -> Session:
        return self.get_or_create_session()

    def get_or_create_session(self) -> Session:
        session = self.get_session()
        if not session:
            return self.create_session()
        return session

    def get_session(self) -> Optional[Session]:
        ctx = self.get_flask_context()
        return getattr(ctx, self.flask_context_key, None)

    def create_session(self) -> Session:
        ctx = self.get_flask_context()
        session = self.SessionMaker(bind=self.engine)
        setattr(ctx, self.flask_context_key, session)
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
