from typing import Union, List
from flask.typing import ResponseReturnValue
from api_boilerplate.utils.blueprint_container import (
    BlueprintContainer, UrlRule, create_route_collector, import_submodules
)
from api_boilerplate.utils.response import error

route_data: List[UrlRule] = []
route = create_route_collector(route_data)

import_submodules(__name__)


class HealthCheck(BlueprintContainer):
    url_rules = route_data

    def error_handler(
            self,
            error_or_code: Union[int, Exception],
    ) -> ResponseReturnValue:
        return error(str(error_or_code))
