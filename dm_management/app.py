from flask import Flask
from dm_management.utils.base_app import BaseApp
from dm_management.healthcheck import HealthCheck


class FlaskApplication(BaseApp):
    def __init__(self) -> None:
        super().__init__(
            name=__name__,
            config_module='dm_management.config',
            flask_options={
                'static_folder': 'static',
                'static_url_path': '/static',
            }
        )

        self.resgister_blueprints()

    def resgister_blueprints(self) -> None:
        self.app.register_blueprint(HealthCheck(url_prefix='').blueprint)


def create_app() -> Flask:
    application = FlaskApplication()
    return application.app


if __name__ == '__main__':
    app = create_app()  # pylint: disable=invalid-name
    app.run('0.0.0.0', debug=app.config['DEBUG'])
