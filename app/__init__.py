from flask import Flask

app = Flask(__name__)

def create_app():
    @app.route("/")
    def home():
        return "Hello world!"

    return app
