import logging
from typing import Union, Optional, Tuple
from flask import Response
from pavlova import PavlovaParsingError
from dm_management.utils.blueprint_container import BluepritContainer, UrlRule
from dm_management.utils import response
from dm_management.v1.user import (
    CreateOrFilterUser,
    GetUserById,
)


class V1(BluepritContainer):
    url_rules = [
        UrlRule(
            route='/user',
            route_name='create_or_filter_user',
            view=CreateOrFilterUser,
        ),
        UrlRule(
            route='/user/<int:user_id>',
            route_name='get_user_by_id',
            view=GetUserById,
        ),
    ]

    error_types = [PavlovaParsingError]

    def error_handler(
            self,
            error_or_code: Union[int, Exception],
    ) -> Optional[Tuple[Response, int]]:
        if isinstance(error_or_code, PavlovaParsingError):
            logging.exception(error_or_code)
            return response.error(
                {
                    'error': str(error_or_code),
                },
                code=422,
            )

        return None
