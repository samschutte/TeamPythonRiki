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

def test_signup_form_and_form_interaction(app):
    client = app.test_client()
    with client:
        # Simulate a user accessing the signup route
        response = client.get('/user/signup/')
        assert response.status_code == 200

        response = client.get('/home/')
        assert b'Home' not in response.data

        # Simulate a user submitting the signup form with valid data
        response = client.post('/user/signup/', data={
            'name': 'new_user',
            'password': '1234',
            'confirm_password': '1234'
        })

        #verify user has assess to restricted page
        response = client.get('/home/')
        assert b'Home' in response.data

        #verify Flask validates input from SignUpFrom 
        user = current_users.get_user('new_user')
        assert user.is_authenticated() is True
