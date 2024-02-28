from flask import Flask


def create_app():
    """Create and configure Flask Application"""
    app = Flask(__name__)

    @app.route('/')
    def root():
        return "Hello World"

    return app
