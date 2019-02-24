from flask.views import MethodView


class PingView(MethodView):
    # pylint: disable=no-self-use
    def get(self) -> str:
        return 'pong'
