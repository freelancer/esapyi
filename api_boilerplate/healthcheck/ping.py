from flask.views import MethodView
from sqlalchemy import text
from api_boilerplate.models.db import db
from api_boilerplate.healthcheck import route


@route('/ping', 'ping')
class PingView(MethodView):
    def get(self) -> str:
        db.session.execute(text('SELECT 1'))
        return 'pong'
