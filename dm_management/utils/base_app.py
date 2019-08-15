from typing import Optional
import os
from flask import Flask
from dm_management.utils.json_encoder import CustomJSONEncoder


class BaseApp:
    app: Flask
    environment: str

    def __init__(
            self,
            name: str,
            config_module: str,
            flask_options: Optional[dict] = None
    ) -> None:
        if flask_options is None:
            flask_options = dict()
        self.config_module = config_module

        self.app = Flask(name, **flask_options)
        self.app.json_encoder = CustomJSONEncoder

        self.configure()

    def resgister_blueprints(self) -> None:
        raise NotImplementedError

    def configure(self) -> None:
        environment_name = os.environ.get('REALM')
        self.app.config.from_object(self.config_module)

        if not environment_name:
            raise Exception(
                'No environment name found.'
                'Cannot configure app.'
            )
        self.environment = environment_name

        self.app.config.from_object(
            f'{self.config_module}.{environment_name}'
        )
