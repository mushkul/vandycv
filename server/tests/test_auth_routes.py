# server/tests/test_auth_routes.py

import unittest
from unittest.mock import patch, MagicMock
import json
import psycopg2
import firebase_admin
from firebase_admin import auth as firebase_auth
from firebase_admin import exceptions as firebase_exceptions
from flask import Flask

class AuthRoutesTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the test client and mock Firebase initialization.
        """
        # Patch Firebase initialization
        patcher_cert = patch('firebase_admin.credentials.Certificate')
        patcher_init = patch('firebase_admin.initialize_app')
        self.mock_cert = patcher_cert.start()
        self.mock_init = patcher_init.start()

        self.addCleanup(patcher_cert.stop)
        self.addCleanup(patcher_init.stop)

        from app import create_app
        app = create_app()
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.auth.routes.firebase_auth.verify_id_token')  # Corrected patch path
    @patch('app.auth.routes.get_db_connection')  # Corrected patch path
    def test_valid_login_existing_user(self, mock_get_db_connection, mock_verify_id_token):
        """
        Test logging in with a valid token where the user already exists in the database.
        """
        # Mock Firebase token verification
        mock_verify_id_token.return_value = {'uid': 'existing_uid', 'email': 'existing@example.com'}

        # Mock database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ('existing_uid',)  # User exists

        # Define test input
        test_payload = {'token': 'valid_token_existing_user'}

        # Make POST request
        response = self.app.post('/login', json=test_payload)  # Adjust to '/auth/login' if url_prefix is used

        # Assertions
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], 'Login successful, user exists in DB')
        self.assertEqual(response_data['email'], 'existing@example.com')
        self.assertEqual(response_data['uid'], 'existing_uid')

        # Ensure database queries were executed correctly
        mock_cursor.execute.assert_called_with('SELECT uid FROM users WHERE uid = %s;', ('existing_uid',))
        mock_conn.close.assert_called_once()

    @patch('app.auth.routes.firebase_auth.verify_id_token')  # Corrected patch path
    @patch('app.auth.routes.get_db_connection')  # Corrected patch path
    def test_valid_login_new_user(self, mock_get_db_connection, mock_verify_id_token):
        """
        Test logging in with a valid token where the user does not exist in the database.
        """
        # Mock Firebase token verification
        mock_verify_id_token.return_value = {'uid': 'new_uid', 'email': 'new@example.com'}

        # Mock database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None  # User does not exist

        # Define test input
        test_payload = {'token': 'valid_token_new_user'}

        # Make POST request
        response = self.app.post('/login', json=test_payload)  # Adjust to '/auth/login' if url_prefix is used

        # Assertions
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], 'Login successful, new user created')
        self.assertEqual(response_data['email'], 'new@example.com')
        self.assertEqual(response_data['uid'], 'new_uid')

        # Ensure database insert was executed
        expected_select_call = unittest.mock.call('SELECT uid FROM users WHERE uid = %s;', ('new_uid',))
        expected_insert_call = unittest.mock.call(
            'INSERT INTO users (uid, email) VALUES (%s, %s);',
            ('new_uid', 'new@example.com')
        )
        mock_cursor.execute.assert_has_calls([expected_select_call, expected_insert_call], any_order=False)
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('app.auth.routes.firebase_auth.verify_id_token')  # Corrected patch path
    def test_missing_token(self, mock_verify_id_token):
        """
        Test logging in without providing a token.
        """
        # Define test input without token
        test_payload = {}

        # Make POST request
        response = self.app.post('/login', json=test_payload)  # Adjust to '/auth/login' if url_prefix is used

        # Assertions
        self.assertEqual(response.status_code, 401)
        response_data = response.get_json()
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['message'], 'Token missing')

        # Ensure Firebase token verification was not called
        mock_verify_id_token.assert_not_called()

    @patch('app.auth.routes.firebase_auth.verify_id_token')  # Corrected patch path
    def test_token_not_string(self, mock_verify_id_token):
        """
        Test logging in with a token that is not a string.
        """
        # Define test input with token as integer
        test_payload = {'token': 12345}

        # Make POST request
        response = self.app.post('/login', json=test_payload)  # Adjust to '/auth/login' if url_prefix is used

        # Assertions
        self.assertEqual(response.status_code, 400)
        response_data = response.get_json()
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['message'], 'Invalid token data type')

        # Ensure Firebase token verification was not called
        mock_verify_id_token.assert_not_called()

    @patch('app.auth.routes.firebase_auth.verify_id_token')  # Corrected patch path
    def test_invalid_json_payload(self, mock_verify_id_token):
        """
        Test logging in with a malformed JSON payload.
        """
        # Define malformed JSON
        malformed_json = "This is not JSON"

        # Make POST request with invalid JSON
        response = self.app.post('/login', data=malformed_json, content_type='application/json')  # Adjust to '/auth/login' if url_prefix is used

        # Assertions
        self.assertEqual(response.status_code, 400)
        response_data = response.get_json()
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['message'], 'Invalid JSON payload')

        # Ensure Firebase token verification was not called
        mock_verify_id_token.assert_not_called()

    @patch('app.auth.routes.firebase_auth.verify_id_token')  # Corrected patch path
    def test_non_json_content_type(self, mock_verify_id_token):
        """
        Test logging in with a non-JSON Content-Type.
        """
        # Define test input
        test_payload = {'token': 'valid_token'}

        # Make POST request with incorrect Content-Type
        response = self.app.post('/login', data=json.dumps(test_payload), content_type='text/plain')  # Adjust to '/auth/login' if url_prefix is used

        # Assertions
        self.assertEqual(response.status_code, 400)
        response_data = response.get_json()
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['message'], 'Invalid JSON payload')

        # Ensure Firebase token verification was not called
        mock_verify_id_token.assert_not_called()

    @patch('app.auth.routes.firebase_auth.verify_id_token')  # Corrected patch path
    def test_invalid_token_type(self, mock_verify_id_token):
        """
        Test logging in with a token of invalid data type (e.g., integer).
        """
        # Define test input with token as integer
        test_payload = {'token': 67890}

        # Make POST request
        response = self.app.post('/login', json=test_payload)  # Adjust to '/auth/login' if url_prefix is used

        # Assertions
        self.assertEqual(response.status_code, 400)
        response_data = response.get_json()
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['message'], 'Invalid token data type')

        # Ensure Firebase token verification was not called
        mock_verify_id_token.assert_not_called()

    @patch('app.auth.routes.firebase_auth.verify_id_token')  # Corrected patch path
    @patch('app.auth.routes.get_db_connection')  # Corrected patch path
    def test_firebase_verification_failure(self, mock_get_db_connection, mock_verify_id_token):
        """
        Test logging in with an invalid token that fails Firebase verification.
        """
        # Mock Firebase to raise FirebaseError
        mock_verify_id_token.side_effect = firebase_admin.exceptions.FirebaseError('Invalid token')

        # Define test input
        test_payload = {'token': 'invalid_token'}

        # Make POST request
        response = self.app.post('/login', json=test_payload)  # Adjust to '/auth/login' if url_prefix is used

        # Assertions
        self.assertEqual(response.status_code, 401)
        response_data = response.get_json()
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['message'], 'Invalid token')

        # Ensure Firebase token verification was called
        mock_verify_id_token.assert_called_once_with('invalid_token')

    @patch('app.auth.routes.firebase_auth.verify_id_token')  # Corrected patch path
    @patch('app.auth.routes.get_db_connection')  # Corrected patch path
    def test_database_connection_failure(self, mock_get_db_connection, mock_verify_id_token):
        """
        Test logging in where the database connection fails.
        """
        # Mock Firebase token verification
        mock_verify_id_token.return_value = {'uid': 'testuid', 'email': 'test@example.com'}

        # Mock database connection to raise psycopg2.Error
        mock_get_db_connection.side_effect = psycopg2.Error('Database connection failed')

        # Define test input
        test_payload = {'token': 'valid_token_database_failure'}

        # Make POST request
        response = self.app.post('/login', json=test_payload)  # Adjust to '/auth/login' if url_prefix is used

        # Assertions
        self.assertEqual(response.status_code, 500)
        response_data = response.get_json()
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['message'], 'Database connection failed')

        # Ensure Firebase token verification was called
        mock_verify_id_token.assert_called_once_with('valid_token_database_failure')

    @patch('app.auth.routes.firebase_auth.verify_id_token')  # Corrected patch path
    @patch('app.auth.routes.get_db_connection')  # Corrected patch path
    def test_database_insert_commit_failure(self, mock_get_db_connection, mock_verify_id_token):
        """
        Test logging in where committing a new user to the database fails.
        """
        # Mock Firebase token verification
        mock_verify_id_token.return_value = {'uid': 'newuid', 'email': 'new@example.com'}

        # Mock database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None  # User does not exist

        # Mock commit to raise an exception
        mock_conn.commit.side_effect = Exception('Commit failed')

        # Define test input
        test_payload = {'token': 'valid_token_commit_failure'}

        # Make POST request
        response = self.app.post('/login', json=test_payload)  # Adjust to '/auth/login' if url_prefix is used

        # Assertions
        self.assertEqual(response.status_code, 500)
        response_data = response.get_json()
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['message'], 'Failed to create user')

        # Ensure database insert was executed
        mock_cursor.execute.assert_called_with(
            'INSERT INTO users (uid, email) VALUES (%s, %s);',
            ('newuid', 'new@example.com')  # Invalid email type
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('app.auth.routes.firebase_auth.verify_id_token')  # Corrected patch path
    def test_token_with_empty_string(self, mock_verify_id_token):
        """
        Test logging in with an empty string as token.
        """
        # Define test input with empty string token
        test_payload = {'token': ''}

        # Make POST request
        response = self.app.post('/login', json=test_payload)  # Adjust to '/auth/login' if url_prefix is used

        # Assertions
        self.assertEqual(response.status_code, 401)
        response_data = response.get_json()
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['message'], 'Token missing')

        # Ensure Firebase token verification was not called
        mock_verify_id_token.assert_not_called()

    @patch('app.auth.routes.firebase_auth.verify_id_token')  # Corrected patch path
    def test_token_as_null(self, mock_verify_id_token):
        """
        Test logging in with a token set to null.
        """
        # Define test input with token as null
        test_payload = {'token': None}

        # Make POST request
        response = self.app.post('/login', json=test_payload)  # Adjust to '/auth/login' if url_prefix is used

        # Assertions
        self.assertEqual(response.status_code, 401)
        response_data = response.get_json()
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['message'], 'Token missing')

        # Ensure Firebase token verification was not called
        mock_verify_id_token.assert_not_called()

if __name__ == '__main__':
    unittest.main()
