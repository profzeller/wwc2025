import os
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config["CONTENT_ROOT"] = "content"

    # Needed for flash() messages used by the assessment form.
    # Set SECRET_KEY in production via environment variable.
    app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")

    from .routes import bp
    app.register_blueprint(bp)

    # Post-assessment + admin results pages
    from .routes_assessment import assessment_bp
    app.register_blueprint(assessment_bp)

    return app
