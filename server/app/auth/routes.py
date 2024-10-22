# app/auth/routes.py
from flask import Blueprint, request, jsonify
import firebase_admin
from firebase_admin import auth as firebase_auth
from firebase_admin import exceptions as firebase_exceptions
from app.db import get_db_connection
import psycopg2

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
        uid = decoded_token['uid']  # Extract the uid from the token
        email = decoded_token['email']  # Get the email from the token

        # Check if the user already exists in the database
        try:
            conn = get_db_connection()
            print("Connected to the database successfully")
        except psycopg2.Error as e:
            print(f"Failed to connect to the database: {e}")
            return jsonify({"success": False, "message": "Database connection failed"}), 500

        cursor = conn.cursor()
        print(f"UID: {uid}, Email: {email}")

        # Query to check if user exists
        cursor.execute('SELECT uid FROM users WHERE uid = %s;', (uid,))
        user_exists = cursor.fetchone()
        print(user_exists)

        if user_exists:
            # User exists, return a success response
            response_message = "Login successful, user exists in DB"
        else:
            # User does not exist, create a new record in the users table
            cursor.execute(
                'INSERT INTO users (uid, email) VALUES (%s, %s);',
                (uid, email)
            )
            try:
                conn.commit()
                print("Changes committed successfully")
            except Exception as e:
                print(f"Error committing to the database: {e}")
            response_message = "Login successful, new user created"

        # Clean up database resources
        cursor.close()
        conn.close()

        print(response_message)

        return jsonify({"success": True, "message": response_message, "email": email, "uid": uid}), 200

    except firebase_exceptions.FirebaseError as e:
        return jsonify({"success": False, "message": str(e)}), 401
