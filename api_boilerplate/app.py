import os
from flask import Flask
from api_boilerplate.utils.base_app import BaseApp
from api_boilerplate.utils.db import wait_for_db
from api_boilerplate.healthcheck import HealthCheck
from api_boilerplate.v1 import V1
from api_boilerplate.models.db import db


# optional imports
has_alembic = False
try:
    from alembic import command as alembic_command
    from alembic.config import Config as AlembicConfig
    has_alembic = True
except ImportError:
    pass


class FlaskApplication(BaseApp):
    def __init__(self) -> None:
        super().__init__(
            name=__name__,
            config_module='api_boilerplate.config',
            flask_options={
                'static_folder': 'static',
                'static_url_path': '/static',
            }
        )

        # initialize all app dependant modules
        db.init_app(
            app=self.app,
            config_connection_key='SQLALCHEMY_DB_URI',
        )

        self.resgister_blueprints()

    def resgister_blueprints(self) -> None:
        self.app.register_blueprint(HealthCheck(url_prefix='').blueprint)
        self.app.register_blueprint(V1(url_prefix='/v1').blueprint)


def run_migrations(app: Flask) -> None:
    with app.app_context():
        alembic_config = AlembicConfig('alembic.ini')
        alembic_command.upgrade(alembic_config, 'head')


def create_app() -> Flask:
    application = FlaskApplication()
    return application.app


if __name__ == '__main__':
    flask_app = create_app()
    assert has_alembic
    print('Waiting for the database to startup')
    wait_for_db(
        db_tcp_addr=os.environ['API_BOILERPLATE_DB_PORT_3306_TCP_ADDR'],
        db_tcp_port=int(os.environ['API_BOILERPLATE_DB_PORT_3306_TCP_PORT']),
    )
    run_migrations(flask_app)
    flask_app.run('0.0.0.0', port=8080, debug=flask_app.config['DEBUG'])
