from sqlalchemy import Column, Integer, String, Text, UniqueConstraint

from api_boilerplate.models.db import Base


class User(Base):
    __tablename__ = 'user'

    __table_args__ = (
        UniqueConstraint(
            'email',
            name='uq_user_email',
        ),
    )

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(256), nullable=False)
    password = Column(Text, nullable=False)
