# app/__init__.py
from flask import Flask  # <-- You need to import Flask
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials

def create_app():
    app = Flask(__name__)
    CORS(app)  # Handle cross-origin requests

    # Initialize Firebase Admin SDK
    cred = credentials.Certificate('vandy-cv-firebase-admin-private-key.json')
    firebase_admin.initialize_app(cred)

    # Import and register blueprints
    from app.auth.routes import auth_bp
    from app.home.routes import home_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(home_bp)

    return app