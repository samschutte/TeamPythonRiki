import pytest
import os
from wiki import create_app

@pytest.fixture
def app():
    directory = os.getcwd()
    test_directory = os.path.join(directory, "tests")
    app = create_app(test_directory)
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection for testing
    return app

def test_search_logic_invalid_tag(app):
    client = app.test_client()

    with client:
        #Log In
        client.post('/user/login/', data={'name': 'test_user', 'password': '1234'},follow_redirects=True)

        #Enter invalid tag
        data = {'one':True}
        response = client.get('/search_by_tags/', data=data, follow_redirects = True)
        #Check routes to correct page 
        assert response.status_code == 200
        assert b'Search By Tags' in response.data

        #Check no test pages apear with tag 'one'
        assert b'Testing_page_1' not in response.data
        assert b'Testing_page_2' not in response.data
        assert b'Testing_page_3' not in response.data

def test_search_log_valid_tag(app):
    client = app.test_client()
    with client:
        client.post('/user/login/', data={'name': 'test_user', 'password': '1234'},follow_redirects=True)

        data = {'interesting': True}
        response = client.get('/search_by_tags/', data=data, follow_redirects = True)
        assert b'Home' in response.data
        
