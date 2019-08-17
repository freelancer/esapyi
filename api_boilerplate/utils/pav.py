from typing import Any
from pavlova.flask import FlaskPavlova
from pavlova.parsers import GenericParser


class Email(str):
    def __new__(cls, input_value: Any) -> str:
        if isinstance(input_value, str):
            if '@' in input_value:
                return str(input_value)
            raise ValueError()
        raise TypeError()


Pavlova = FlaskPavlova()

# setup parsers
Pavlova.register_parser(Email, GenericParser(Pavlova, Email))
