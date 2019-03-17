from typing import Tuple
from dataclasses import asdict
from flask import Response
from flask.views import MethodView

from dm_management.handlers.user import create_user
from dm_management.utils.pav import Pavlova
from dm_management.v1.input_schemas import User as UserInput
from dm_management.v1.output_schemas import User as UserSchema
from dm_management.utils import response


class CreateOrFilterUser(MethodView):
    @Pavlova.use(UserInput)
    def post(self, data: UserInput) -> Tuple[Response, int]:
        user = create_user(
            email=data.email,
            password=data.password,
        )

        return response.ok(asdict(UserSchema.from_model(user)))
