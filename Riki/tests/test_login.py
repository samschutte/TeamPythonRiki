import pytest
import os
from wiki import create_app

# Initialize your app for testing
@pytest.fixture
def app():
    directory = os.getcwd()
    test_directory = os.path.join(directory, "tests")
    app = create_app(test_directory)
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection for testing
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# Test GET request to the login page
def test_user_login_page(client):
    response = client.get('/user/login/')
    assert response.status_code == 200
    assert b'Login' in response.data  # Check if the login form is displayed

# Test POST request with valid data
def test_valid_user_login(client):
    data = {'name': 'test_user', 'password': '1234'}
    response = client.post('/user/login/', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Login successful' in response.data  # Check for a success message

 # Test POST request with invalid data (incorrect password)
def test_invalid_user_login(client):
    data = {'name': 'test_user', 'password': '1235'}
    response = client.post('/user/login/', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Errors occured verifying your input. Please check the marked fields below.' in response.data