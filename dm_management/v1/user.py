from typing import Tuple
from dataclasses import asdict
from flask import Response
from flask.views import MethodView

from dm_management.handlers.user import (
    create_user,
    get_user_by_id,
    get_user_by_email,
)
from dm_management.utils.pav import Pavlova
from dm_management.v1.input_schemas import (
    User as UserInput,
    UserFilter as UserFilterInput,
)
from dm_management.v1.output_schemas import (
    UserSchema,
    UserListSchema,
    SingleErrorSchema,
)
from dm_management.utils import response
from dm_management.exceptions.user import (
    UserAlreadyExistsException,
    UserNotFoundException,
)


class CreateOrFilterUser(MethodView):
    @Pavlova.use(UserFilterInput)
    def get(self, data: UserFilterInput) -> Tuple[Response, int]:
        try:
            user = get_user_by_email(email=data.email)
            return response.ok(asdict(UserListSchema(users=[
                UserSchema.from_model(user),
            ])))
        except UserNotFoundException:
            return response.not_found(asdict(SingleErrorSchema(
                error=f'User with email {data.email} was not found'
            )))

    @Pavlova.use(UserInput)
    def post(self, data: UserInput) -> Tuple[Response, int]:
        try:
            user = create_user(
                email=data.email,
                password=data.password,
            )
            return response.ok(asdict(UserSchema.from_model(user)))
        except UserAlreadyExistsException:
            return response.bad_request(asdict(SingleErrorSchema(
                error=f'User with email {data.email} already exists'
            )))


class GetUserById(MethodView):
    def get(self, user_id: int) -> Tuple[Response, int]:
        try:
            user = get_user_by_id(user_id=user_id)
            return response.ok(asdict(UserSchema.from_model(user)))
        except UserNotFoundException:
            return response.not_found(asdict(SingleErrorSchema(
                error=f'User with id {user_id} was not found'
            )))
