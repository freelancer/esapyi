from flask.views import MethodView
from api_boilerplate.models.db import db


class PingView(MethodView):
    def get(self) -> str:
        db.session.execute('SELECT 1')
        return 'pong'
