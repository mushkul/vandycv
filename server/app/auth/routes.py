# app/auth/routes.py
from flask import Blueprint, request, jsonify
import firebase_admin
from firebase_admin import auth as firebase_auth
from firebase_admin import exceptions as firebase_exceptions

# Define a blueprint for authentication-related routes
auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    id_token = data.get('token')  # Expecting the token from the frontend

    if not id_token:
        return jsonify({"success": False, "message": "Token missing"}), 401

    try:
        # Verify the token using Firebase Admin SDK
        decoded_token = firebase_auth.verify_id_token(id_token)
        email = decoded_token['email']  # Get the email from the token
        return jsonify({"success": True, "message": "Login successful", "email": email}), 200
    except firebase_exceptions.FirebaseError as e:
        return jsonify({"success": False, "message": str(e)}), 401