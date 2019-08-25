from typing import Optional
from flask import Flask
from api_boilerplate.utils.json_encoder import CustomJSONEncoder


class BaseApp:
    app: Flask

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
        # loads config from the __init__.py file in the modile
        self.app.config.from_object(self.config_module)

        environment_name = self.app.config['ENVIRONMENT']
        if not environment_name:
            raise Exception(
                'No environment name found.'
                'Cannot configure app.'
            )

        # load environment specific config
        self.app.config.from_object(
            f'{self.config_module}.{environment_name}'
        )

        # load external config
        external_config_directory = self.app.config[
            'EXTERNAL_CONFIG_DIRECTORY'
        ]
        if external_config_directory:
            self.app.config.from_json(
                f'{external_config_directory}/config.json'
            )