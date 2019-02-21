from flask import Flask
from dm_management.utils.base_app import BaseApp


class FlaskApplication(BaseApp):
    def __init__(self) -> None:
        super().__init__(
            name=__name__,
            flask_options={
                'static_folder': 'static',
                'static_url_path': '/static',
            }
        )


def create_app() -> Flask:
    application = FlaskApplication()
    return application.app


if __name__ == '__main__':
    app = create_app()
    app.run('0.0.0.0', debug=True)
