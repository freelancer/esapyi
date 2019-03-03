from flask.views import MethodView
from dm_management.models.db import db


class PingView(MethodView):
    # pylint: disable=no-self-use
    def get(self) -> str:
        db.session.execute('SELECT 1')
        return 'pong'
