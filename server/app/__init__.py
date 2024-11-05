# app/__init__.py
from flask import Flask, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials
from openai import OpenAI
import json
import openai
import os


def create_app():
    app = Flask(__name__)
    CORS(app)
    # CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    @app.route("/")
    def index():
        return "Welcome to the Flask API!", 200

    # Load the API key from vandy-cv-openai-key.json
    config_path = os.path.join(app.root_path, '..', 'vandy-cv-openai-key.json')
    try:
        with open(config_path) as config_file:
            config = json.load(config_file)
            openai_api_key = config.get('OPENAI_API_KEY')
    except FileNotFoundError:
        raise FileNotFoundError(
            "Configuration file 'vandy-cv-openai-key.json' not found.")

    # print("\n\n\n", openai_api_key, "\n\n\n")
    # Ensure the API key is available
    if not openai_api_key:
        raise ValueError(
            "OpenAI API key not found in 'cvandy-cv-openai-key.json'.")

    # Set the OpenAI API key
    os.environ["OPENAI_API_KEY"] = openai_api_key

    # openai.api_key = openai_api_key

    # Initialize Firebase Admin SDK
    cred = credentials.Certificate('vandy-cv-firebase-admin-private-key.json')
    firebase_admin.initialize_app(cred)

    # Import and register blueprints
    from app.auth.routes import auth_bp
    from app.home.routes import home_bp
    from app.resume.routes import resume_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(home_bp)
    app.register_blueprint(resume_bp)

    return app
