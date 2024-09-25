# app/auth/routes.py
from flask import Blueprint, request, jsonify

# Define a blueprint for authentication-related routes
auth_bp = Blueprint('auth_bp', __name__)

# Dummy user data (this could come from a database in a real app)
users = {
    "balamia@gmail.com": "securepassword",
}


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Validate credentials
    if email in users and users[email] == password:
        return jsonify({"success": True, "message": "Login successful"}), 200
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401
