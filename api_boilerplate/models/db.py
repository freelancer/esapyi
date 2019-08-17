from sqlalchemy.ext.declarative import declarative_base

from api_boilerplate.utils.flask_sqlalchemy import SqlAlchemy as FlaskSqlAlchemy


db = FlaskSqlAlchemy()

Base = declarative_base()
