import unittest
from flask import Flask, jsonify, request
from unittest.mock import patch, MagicMock
from server import app


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('firebase_admin.auth.create_user')
    def test_valid_user_registration(self, mock_create_user):
        # Mock the response from Firebase
        mock_create_user.return_value = MagicMock(uid='testuid')

        # Define test input
        test_data = {
            'email': 'validuser@example.com',
            'password': 'validpassword'
        }

        # Make POST request to the registration endpoint
        response = self.app.post('/register', json=test_data)

        # Assert the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)

    def test_form_submission_with_required_fields(self):
        # Test data with required fields
        test_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'answer1': 'Sample Answer',
            'answer2': 'Another Answer'
        }

        # Make POST request to the form submission endpoint
        response = self.app.post('/submit', json=test_data)

        # Assert the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Form submitted successfully', response.data)


if __name__ == '__main__':
    unittest.main()
