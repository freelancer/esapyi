from typing import Tuple

import flask
from flask import jsonify


def _response(response: object, code: int) -> Tuple[flask.Response, int]:
    return jsonify(response), code


def ok(response: object = None, code: int = 200) -> Tuple[flask.Response, int]:
    return _response(response, code)


def created(
        response: object = None, code: int = 201
) -> Tuple[flask.Response, int]:
    return _response(response, code)


def no_content(
        response: object = None, code: int = 204
) -> Tuple[flask.Response, int]:
    return _response(response, code)


def bad_request(
        response: object = None, code: int = 400
) -> Tuple[flask.Response, int]:
    return _response(response, code)


def forbidden(
        response: object = None, code: int = 403
) -> Tuple[flask.Response, int]:
    return _response(response, code)


def not_found(
        response: object = None, code: int = 404
) -> Tuple[flask.Response, int]:
    return _response(response, code)

def conflict(
        response: object = None, code: int = 409
) -> Tuple[flask.Response, int]:
    return _response(response, code)


def error(
        response: object = None,
        code: int = 500
) -> Tuple[flask.Response, int]:
    return _response(response, code)
