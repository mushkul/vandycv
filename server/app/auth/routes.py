# app/auth/routes.py
from flask import Blueprint, request, jsonify
import firebase_admin
from firebase_admin import auth as firebase_auth
from firebase_admin import exceptions as firebase_exceptions

# Define a blueprint for authentication-related routes
auth_bp = Blueprint('auth_bp', __name__)

# Dummy user data for example purposes (this could come from a database in a real app)
users = {
    "balamia@gmail.com": "securepassword",
    "adam@example.com": "mypassword123",
    "stanley@example.com": "password456"
}

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

        # Check if the email is in the dummy data (or check against a real database)
        if email in users:
            # For demonstration purposes, we will return the dummy user's info
            return jsonify({"success": True, "message": "Login successful", "email": email}), 200
        else:
            return jsonify({"success": False, "message": "User not found"}), 404

    except firebase_exceptions.FirebaseError as e:
        return jsonify({"success": False, "message": str(e)}), 401