from dataclasses import dataclass
from dm_management.utils.pav import Email


@dataclass
class User:
    email: Email
    password: str


@dataclass
class UserFilter:
    email: Email
