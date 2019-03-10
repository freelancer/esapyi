from sqlalchemy import Column, Integer, String, Text, Index

from dm_management.models.db import Base


class User(Base):
    __tablename__ = 'user'

    __table_args__ = (
        Index(
            'idx_user_email',
            'email',
        ),
    )

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(256), nullable=False)
    password = Column(Text, nullable=False)
