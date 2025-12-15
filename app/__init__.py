from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config["CONTENT_ROOT"] = "content"

    from .routes import bp
    app.register_blueprint(bp)

    return app
