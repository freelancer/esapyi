from dataclasses import dataclass
from api_boilerplate.utils.pav import Email


@dataclass
class User:
    email: Email
    password: str


@dataclass
class UserFilter:
    email: Email
