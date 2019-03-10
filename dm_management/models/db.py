from sqlalchemy.ext.declarative import declarative_base

from dm_management.utils.flask_sqlalchemy import SqlAlchemy as FlaskSqlAlchemy


db = FlaskSqlAlchemy()

Base = declarative_base()
