from sqlalchemy import String, Text, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from api_boilerplate.models.db import Base


class User(Base):
    __tablename__ = 'user'

    __table_args__ = (
        UniqueConstraint(
            'email',
            name='uq_user_email',
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    email = mapped_column(String(256), nullable=False)
    password = mapped_column(Text, nullable=False)
