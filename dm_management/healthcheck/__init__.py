from typing import Union, Optional, Tuple
from flask import Response
from dm_management.utils.blueprint_container import BluepritContainer, UrlRule
from dm_management.healthcheck.ping import PingView


class HealthCheck(BluepritContainer):
    url_rules = [
        UrlRule(
            route='/ping',
            route_name='ping',
            view=PingView,
        )
    ]

    error_types = [Exception]
