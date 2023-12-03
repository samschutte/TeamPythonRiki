import pytest
import os
from wiki import create_app
from wiki.web.file_handler import FileHandler


@pytest.fixture
def app():
    directory = os.getcwd()
    test_directory = os.path.join(directory, "tests")
    app = create_app(test_directory)
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection for testing
    return app

class File1:
    filename = ""
    stream = ""
    def __init__(self,filename):
        self.filename = filename

def test_route(app):
    client = app.test_client()
    with client:
        #login 
        client.post('/user/login/', data={'name': 'test_user', 'password': '1234'},follow_redirects=True)

        #upload a fake file to check correct route 
        response = client.get('/edit/home', follow_redirects=True)
        response = client.post('/edit/home/', data = {'file': File1('test.png')}, follow_redirects=True)
        assert response.status_code == 200 
    
def test_file_handler(app):
    client = app.test_client()
    with client:
        client.post('/user/login/', data={'name': 'test_user', 'password': '1234'},follow_redirects=True)

        response = client.get('edit/home', follow_redirects=True)
        response = client.post('/edit/home/',data = {'file': File1("")}, follow_redirects=True)
        # adding a file without a .filetype at the end should not add file 
        home_path = os.path.join(app.config['CONTENT_DIR'], 'home.md')
        with open(home_path, 'r') as f:
            content = f.read()
        assert response.status_code ==200
        assert 'files:' not in content
    


