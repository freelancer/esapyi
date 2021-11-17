from typing import List, Type, Optional, Tuple, NamedTuple, no_type_check
from flask import Blueprint, Response
from flask.views import MethodView


class UrlRule(NamedTuple):
    route: str
    route_name: str
    view: Type[MethodView]


class BluepritContainer:
    blueprint: Blueprint
    url_rules: List[UrlRule] = []
    error_types: List[Type[Exception]] = []

    def __init__(self, url_prefix: str) -> None:
        self.name = f'{self.__class__.__name__}-{url_prefix}'
        self.blueprint = Blueprint(
            name=self.name,
            import_name=__name__,
            url_prefix=url_prefix,
        )

        for rule in self.url_rules:
            self.blueprint.add_url_rule(
                rule.route,
                view_func=rule.view.as_view(rule.route_name),
            )

        for error in self.error_types:
            self.blueprint.register_error_handler(error, self.error_handler)

    @no_type_check
    def error_handler(
            self,
            error_or_code: Exception,
    ) -> Optional[Tuple[Response, int]]:
        raise NotImplementedError
