import importlib
import pkgutil
from typing import List, Type, NamedTuple, Callable
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


def import_submodules(package, recursive=True):
    """ Import all submodules of a module, recursively, including subpackages

    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for _, name, is_pkg in pkgutil.walk_packages(
            package.__path__,
            package.__name__ + '.'
    ):
        results[name] = importlib.import_module(name)
        if recursive and is_pkg:
            results.update(import_submodules(name))
    return results


def create_route_collector(data_array: List[UrlRule]) -> Callable[
        [str, str], Callable[[Type[MethodView]], Type[MethodView]]
]:
    route_array = data_array
    def route(path: str, view_name: str) -> Callable[[Type[MethodView]], Type[MethodView]]:
        def wrap(cls: Type[MethodView]) -> Type[MethodView]:
            nonlocal route_array
            route_array.append(UrlRule(path, view_name, cls))
            return cls
        return wrap
    return route
