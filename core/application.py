from flask import Flask


class Application:

    def __init__(self):
        self.app = Flask(__name__)

    def setConfig(self, launch=False):
        from config import Routes
        if launch:
            self.app.run(debug=True)
