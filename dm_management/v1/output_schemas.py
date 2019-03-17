from dataclasses import dataclass
from pavlova import PavlovaParsingError
from dm_management.utils.pav import Pavlova, Email
from dm_management.models.user import User as UserModel


class OutputSchemaBuildException(Exception):
    pass


@dataclass
class User:
    id: int
    email: Email
    password: str

    @staticmethod
    def from_model(model: UserModel) -> 'User':
        try:
            return Pavlova.from_mapping({
                'id': model.id,
                'email': model.email,
                'password': model.password,
            }, User)
        except PavlovaParsingError:
            raise OutputSchemaBuildException()
