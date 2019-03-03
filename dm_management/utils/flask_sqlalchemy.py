from typing import Optional
from flask import Flask
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

    def __init__(
            self,
            pool_class: Optional[Pool] = None
    ) -> None:
        self.override_pool_class = pool_class
        self.SessionMaker = sessionmaker()  # pylint: disable=invalid-name

    def init_app(self, app: Flask, config_connection_key: str) -> None:
        if self.override_pool_class:
            self.engine = create_engine(
                app.config[config_connection_key],
                pool_class=self.override_pool_class,
            )
        else:
            self.engine = create_engine(app.config[config_connection_key])

        self.SessionMaker.configure(bind=self.engine)

    @property
    def session(self) -> Session:
        return self.SessionMaker()
