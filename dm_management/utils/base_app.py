from typing import Optional
from flask import Flask
from dm_management.utils.json_encoder import CustomJSONEncoder


class BaseApp:
    app: Flask

    def __init__(
            self,
            name: str,
            flask_options: Optional[dict] = None
    ) -> None:
        if flask_options is None:
            flask_options = dict()

        self.app = Flask(name, **flask_options)
        self.app.json_encoder = CustomJSONEncoder
