# app/__init__.py
from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)  # Handle cross-origin requests

    # Import and register blueprints
    from app.auth.routes import auth_bp
    from app.home.routes import home_bp
    # from app.dashboard.routes import dashboard_bp
    # from app.profile.routes import profile_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(home_bp)

    # app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    # app.register_blueprint(profile_bp, url_prefix='/profile')

    return app
