from typing import List
from dataclasses import dataclass
from pavlova import PavlovaParsingError
from api_boilerplate.utils.pav import Pavlova, Email
from api_boilerplate.models.user import User as UserModel


class OutputSchemaBuildException(Exception):
    pass


@dataclass
class UserSchema:
    id: int
    email: Email
    password: str

    @staticmethod
    def from_model(model: UserModel) -> 'UserSchema':
        try:
            return Pavlova.from_mapping({
                'id': model.id,
                'email': model.email,
                'password': model.password,
            }, UserSchema)
        except PavlovaParsingError:
            raise OutputSchemaBuildException()


@dataclass
class UserListSchema:
    users: List[UserSchema]


@dataclass
class SingleErrorSchema:
    error: str
