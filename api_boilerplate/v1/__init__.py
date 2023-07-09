import logging
from typing import Union, Optional, Tuple, List
from flask import Response
from pavlova import PavlovaParsingError
from api_boilerplate.utils.blueprint_container import (
    BlueprintContainer, UrlRule, create_route_collector, import_submodules
)
from api_boilerplate.utils import response

route_data: List[UrlRule] = []
route = create_route_collector(route_data)

import_submodules(__name__)


class V1(BlueprintContainer):
    url_rules = route_data
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
