from flask import Flask

class BaseApp:
    app: Flask

    def __init__(self, name: str) -> None:
        self.app = Flask(name)
