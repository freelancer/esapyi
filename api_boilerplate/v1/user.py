from dataclasses import asdict
from flask.views import MethodView
from flask.typing import ResponseReturnValue

from api_boilerplate.handlers.user import (
    create_user,
    get_user_by_id,
    get_user_by_email,
)
from api_boilerplate.utils.pav import Pavlova
from api_boilerplate.v1 import route
from api_boilerplate.v1.input_schemas import (
    User as UserInput,
    UserFilter as UserFilterInput,
)
from api_boilerplate.v1.output_schemas import (
    UserSchema,
    UserListSchema,
    SingleErrorSchema,
)
from api_boilerplate.utils import response
from api_boilerplate.exceptions.user import (
    UserAlreadyExistsException,
    UserNotFoundException,
)


@route('/user', 'create_or_filter_user')
class CreateOrFilterUser(MethodView):
    @Pavlova.use(UserFilterInput)
    def get(self, data: UserFilterInput) -> ResponseReturnValue:
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
    def post(self, data: UserInput) -> ResponseReturnValue:
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


@route('/user/<int:user_id>', 'get_user_by_id')
class GetUserById(MethodView):
    def get(self, user_id: int) -> ResponseReturnValue:
        try:
            user = get_user_by_id(user_id=user_id)
            return response.ok(asdict(UserSchema.from_model(user)))
        except UserNotFoundException:
            return response.not_found(asdict(SingleErrorSchema(
                error=f'User with id {user_id} was not found'
            )))
