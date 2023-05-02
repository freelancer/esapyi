from sqlalchemy.orm import DeclarativeBase

from api_boilerplate.utils.flask_sqlalchemy import SqlAlchemy as FlaskSqlAlchemy


db = FlaskSqlAlchemy()

class Base(DeclarativeBase):
    pass
