# server/tests/test_endpoints.py

import pytest
from unittest.mock import patch, MagicMock


# Define a fixture to mock Firebase initialization and provide a test client
@pytest.fixture
def client():
    # Mock firebase_admin.credentials.Certificate and firebase_admin.initialize_app
    with patch('firebase_admin.credentials.Certificate') as mock_certificate, \
         patch('firebase_admin.initialize_app') as mock_initialize_app:
        
        # Configure the mocks
        mock_certificate.return_value = MagicMock()
        mock_initialize_app.return_value = MagicMock()

        # Import the app **after** mocking Firebase to ensure mocks are in place
        from app import create_app  # Adjust the import path based on your project structure
        app = create_app()
        app.config['TESTING'] = True

        # Create a test client using the Flask application configured for testing
        with app.test_client() as client:
            yield client


# Define a fixture to mock generate_resume_text function
@pytest.fixture
def mock_generate_resume_text():
    with patch('app.resume.routes.generate_resume_text') as mock_func:
        yield mock_func


# Test case for successful resume generation
def test_generate_resume_endpoint(client, mock_generate_resume_text):
    # Mock the generate_resume_text function
    mock_generate_resume_text.return_value = "Generated Resume Content"

    # Define test input; ensure 'body' is a JSON string as expected by the route
    test_data = {
        'body': '{"firstName": "Alice", "middleInitial": "A", "lastName": "Doe", "address": "123 Main St", "email": "alice@example.com", "contactNumber": "123-456-7890", "linkedinLink": "https://linkedin.com/in/alicedoe", "githubLink": "https://github.com/alicedoe", "college": "Vanderbilt University", "majorConcentration": "Computer Science", "secondMajor": "Mathematics", "gpa": "4.0", "locationOfCollege": "Nashville, TN", "startYear": "2018", "endYear": "2022", "relevantCoursework": "Algorithms, Data Structures", "jobExperiences": [{"name": "Company A", "title": "Software Engineer", "location": "Nashville, TN", "description": "Developed web applications."}]}'  # 'body' is a JSON string
    }

    # Make POST request to the generate_resume endpoint
    response = client.post('/generateresume/', json=test_data)

    # Assert the response is correct
    assert response.status_code == 200
    assert b'Generated Resume Content' in response.data


# Test case for failed resume generation due to missing fields
def test_generate_resume_fail_missing_fields(client, mock_generate_resume_text):
    # Define test input with missing required fields
    test_data = {
        'body': '{"firstName": "Alice", "email": "alice@example.com"}'  # Missing many fields
    }

    # Make POST request to the generate_resume endpoint
    response = client.post('/generateresume/', json=test_data)

    # Assert the response indicates a bad request
    assert response.status_code == 400
    assert b'Missing required fields' in response.data


# Test case for failed resume generation due to invalid email format
def test_generate_resume_fail_invalid_email(client, mock_generate_resume_text):
    # Define test input with invalid email format
    test_data = {
        'body': '{"firstName": "Alice", "middleInitial": "A", "lastName": "Doe", "address": "123 Main St", "email": "invalidemail", "contactNumber": "123-456-7890", "linkedinLink": "https://linkedin.com/in/alicedoe", "githubLink": "https://github.com/alicedoe", "college": "Vanderbilt University", "majorConcentration": "Computer Science", "secondMajor": "Mathematics", "gpa": "4.0", "locationOfCollege": "Nashville, TN", "startYear": "2018", "endYear": "2022", "relevantCoursework": "Algorithms, Data Structures", "jobExperiences": [{"name": "Company A", "title": "Software Engineer", "location": "Nashville, TN", "description": "Developed web applications."}]}'  # Invalid email
    }

    # Make POST request to the generate_resume endpoint
    response = client.post('/generateresume/', json=test_data)

    # Assert the response indicates a bad request
    assert response.status_code == 400
    assert b'Invalid email format' in response.data


# Test case for resume generation with extra fields (should ignore or handle gracefully)
def test_generate_resume_extra_fields(client, mock_generate_resume_text):
    # Mock the generate_resume_text function
    mock_generate_resume_text.return_value = "Generated Resume Content with Extra Fields"

    # Define test input with extra fields not required by the endpoint
    test_data = {
        'body': '{"firstName": "Alice", "middleInitial": "A", "lastName": "Doe", "address": "123 Main St", "email": "alice@example.com", "contactNumber": "123-456-7890", "linkedinLink": "https://linkedin.com/in/alicedoe", "githubLink": "https://github.com/alicedoe", "college": "Vanderbilt University", "majorConcentration": "Computer Science", "secondMajor": "Mathematics", "gpa": "4.0", "locationOfCollege": "Nashville, TN", "startYear": "2018", "endYear": "2022", "relevantCoursework": "Algorithms, Data Structures", "jobExperiences": [{"name": "Company A", "title": "Software Engineer", "location": "Nashville, TN", "description": "Developed web applications."}], "age": 30}'  # Extra field 'age'
    }

    # Make POST request to the generate_resume endpoint
    response = client.post('/generateresume/', json=test_data)

    # Assert the response handles extra fields appropriately
    assert response.status_code == 200
    assert b'Generated Resume Content with Extra Fields' in response.data


# Test case for resume generation with invalid data types
def test_generate_resume_invalid_data_types(client, mock_generate_resume_text):
    # Define test input with invalid data types for 'jobExperiences'
    test_data = {
        'body': '{"firstName": "Alice", "middleInitial": "A", "lastName": "Doe", "address": "123 Main St", "email": "alice@example.com", "contactNumber": "123-456-7890", "linkedinLink": "https://linkedin.com/in/alicedoe", "githubLink": "https://github.com/alicedoe", "college": "Vanderbilt University", "majorConcentration": "Computer Science", "secondMajor": "Mathematics", "gpa": "4.0", "locationOfCollege": "Nashville, TN", "startYear": "2018", "endYear": "2022", "relevantCoursework": "Algorithms, Data Structures", "jobExperiences": "Should be a list, not a string"}'  # Invalid data type for 'jobExperiences'
    }

    # Make POST request to the generate_resume endpoint
    response = client.post('/generateresume/', json=test_data)

    # Assert the response indicates a bad request
    assert response.status_code == 400
    assert b'Invalid data type for jobExperiences' in response.data


# Test case for handling server errors during resume generation
def test_generate_resume_server_error(client, mock_generate_resume_text):
    # Mock generate_resume_text to raise an exception
    mock_generate_resume_text.side_effect = Exception('Unexpected server error')

    # Define test input
    test_data = {
        'body': '{"firstName": "Alice", "middleInitial": "A", "lastName": "Doe", "address": "123 Main St", "email": "alice@example.com", "contactNumber": "123-456-7890", "linkedinLink": "https://linkedin.com/in/alicedoe", "githubLink": "https://github.com/alicedoe", "college": "Vanderbilt University", "majorConcentration": "Computer Science", "secondMajor": "Mathematics", "gpa": "4.0", "locationOfCollege": "Nashville, TN", "startYear": "2018", "endYear": "2022", "relevantCoursework": "Algorithms, Data Structures", "jobExperiences": [{"name": "Company A", "title": "Software Engineer", "location": "Nashville, TN", "description": "Developed web applications."}]}'  # 'body' is a JSON string
    }

    # Make POST request to the generate_resume endpoint
    response = client.post('/generateresume/', json=test_data)

    # Assert the response indicates internal server error
    assert response.status_code == 500
    assert b'Internal server error' in response.data


# Test case for accessing an invalid endpoint
def test_invalid_endpoint(client):
    """
    Test accessing an endpoint that doesn't exist.
    """
    response = client.get('/nonexistent')
    assert response.status_code == 404
    assert 'error' in response.json
    assert response.json['error'] == 'Not Found'


# Test case for method not allowed
def test_method_not_allowed(client):
    """
    Test sending a GET request to a POST-only endpoint.
    """
    response = client.get('/generateresume/')
    assert response.status_code == 405
    assert 'error' in response.json
    assert response.json['error'] == 'Method Not Allowed'


# Parameterized test for various invalid inputs
@pytest.mark.parametrize("test_input, expected_status, expected_error", [
    (
        {"body": '{"firstName": "Alice", "email": "alice@example.com"}'},  # Missing 'education' and 'skills'
        400,
        "Missing required fields"
    ),
    (
        {"body": '{"firstName": "Alice", "email": "invalidemail", "education": [], "skills": []}'},  # Invalid email
        400,
        "Invalid email format"
    ),
    (
        {"body": '{"firstName": "", "email": "alice@example.com", "education": [], "skills": []}'},  # Empty name
        400,
        "Fields cannot be empty"
    ),
])
def test_generate_resume_invalid_inputs(client, test_input, expected_status, expected_error):
    """
    Parameterized test for various invalid input scenarios.
    """
    response = client.post('/generateresume/', json=test_input)
    assert response.status_code == expected_status
    assert expected_error.encode() in response.data