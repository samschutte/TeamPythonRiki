import pytest
import os
from wiki import create_app
from wiki.web.reference_handler import ReferenceHandler

@pytest.fixture
def app():
    directory = os.getcwd()
    test_directory = os.path.join(directory, "tests")
    app = create_app(test_directory)
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection for testing
    return app

def test_reference_form(app):
    client = app.test_client()

    with client:
        client.post('/user/login/', data={'name': 'test_user', 'password': '1234'},follow_redirects=True)
        
        #check that editor form now has reference option
        response = client.get('/edit/home', follow_redirects = True)
        assert b'Wiki Editor' in response.data
        assert b'Reference Title' in response.data
        assert b'Reference Author' in response.data

        data ={'referenceTitle': 'Sam', 'referenceAuthor': 'S'}
        response = client.post('/edit/home/', data=data, follow_redirects=True)
        response = client.get('/home/')
        
        assert b'References:' in response.data
    

