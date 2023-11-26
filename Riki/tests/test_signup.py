import pytest
import os
from wiki import create_app
from wiki.web import current_users

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

@pytest.fixture(autouse=True)
def cleanup_new_test_user(app):
    yield
    with app.app_context():
        current_users.delete_user('new_user')

def test_signup_page_access(client):
    response = client.get('/user/signup/')
    assert response.status_code == 200
    assert b'Sign Up' in response.data

def test_signup_page_input_fields(client):
    response = client.get('/user/signup/')
    assert b'Username' in response.data
    assert b'Password' in response.data
    assert b'Confirm Password' in response.data

def test_signup_existing_username(client):
    data = {'name': 'test_user', 'password': '1234', 'confirm_password': '1234'}
    response = client.post('/user/signup/', data=data, follow_redirects=True)
    assert b'Errors occured verifying your input. Please check the marked fields below.' in response.data
    assert b'This username already exists' in response.data

def test_signup_nonmatch_password(client):
    data = {'name': 'new_user', 'password': '1234', 'confirm_password': '123'}
    response = client.post('/user/signup/', data=data, follow_redirects=True)
    assert b'Errors occured verifying your input. Please check the marked fields below.' in response.data
    assert b'Password must match' in response.data

def test_signup_valid(client, app):
    data = {'name': 'new_user', 'password': '1234', 'confirm_password': '1234'}
    response = client.post('/user/signup/', data=data, follow_redirects=True)
    assert b'Sign Up Successful' in response.data
    with app.app_context():
        user = current_users.get_user('new_user')
        assert user is not None

def test_automatic_login_with_valid_signup(client, app):
    data = {'name': 'new_user', 'password': '1234', 'confirm_password': '1234'}
    client.post('/user/signup/', data=data, follow_redirects=True)
    with app.app_context():
        user = current_users.get_user('new_user')
        userIsLoggedIn = user.is_authenticated()
        assert userIsLoggedIn is True

