from typing import List, Type, NamedTuple
from flask import Blueprint
from flask.typing import ResponseReturnValue
from flask.views import MethodView


class UrlRule(NamedTuple):
    route: str
    route_name: str
    view: Type[MethodView]


class BlueprintContainer:
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

    def error_handler(
            self,
            error_or_code: Exception,
    ) -> ResponseReturnValue:
        raise NotImplementedError
