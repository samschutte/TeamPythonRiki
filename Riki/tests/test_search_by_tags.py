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

def test_user_login_route(app):
    client = app.test_client()

    # Test authenticated feature
    with client:
        # Simulate signing in
        client.post('/user/login/', data={'name': 'test_user', 'password': '1234'},follow_redirects=True)
        
        # Now, test an authenticated route
        response = client.get('/search_by_tags', follow_redirects=True)
        assert response.status_code == 200
        assert b'tag1' in response.data
        assert b'Search By Tags' in response.data
        
        # Test POST request to the search_by_tags route with valid form data
        data = {'tag1':True}
        response = client.post('/search_by_tags/', data=data, follow_redirects=True)
        assert response.status_code == 200
        assert b'Results for <i>tag1</i>' in response.data
        assert b'Testing_page_1' in response.data
        assert b'Testing_page_2' in response.data
        assert b'Testing_page_3' in response.data

        # Test POST request to the search_by_tags route with valid form data
        data = {'tag1':True, 'tag2':True}
        response = client.post('/search_by_tags/', data=data, follow_redirects=True)
        assert response.status_code == 200
        assert b'Results for <i>tag1, tag2</i>' in response.data
        assert b'Testing_page_1' not in response.data
        assert b'Testing_page_2' in response.data
        assert b'Testing_page_3' in response.data

                # Test POST request to the search_by_tags route with valid form data
        data = {'tag1':True, 'tag2':True, 'tag3':True}
        response = client.post('/search_by_tags/', data=data, follow_redirects=True)
        assert response.status_code == 200
        assert b'Results for <i>tag1, tag2, tag3</i>' in response.data
        assert b'Testing_page_1' not in response.data
        assert b'Testing_page_2' not in response.data
        assert b'Testing_page_3' in response.data