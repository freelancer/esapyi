from typing import Union, Optional, Tuple
from flask import Response
from api_boilerplate.utils.blueprint_container import BlueprintContainer, UrlRule
from api_boilerplate.healthcheck.ping import PingView


class HealthCheck(BlueprintContainer):
    url_rules = [
        UrlRule(
            route='/ping',
            route_name='ping',
            view=PingView,
        )
    ]

    def error_handler(
            self,
            error_or_code: Union[int, Exception],
    ) -> Optional[Tuple[Response, int]]:
        pass
