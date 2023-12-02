import pytest
from wiki.web.file_handler import FileHandler

class FakeFile:
    filename = ""
    stream = ""
    def __init__(self, filename):
        self.filename = filename
 
class FakePage:
    url = ""
    def __init__(self):
        pass

def test_FileHandler_image():
    fakePage = FakePage()
    fakeFile = FakeFile("image.png")
    fileHandler = FileHandler(fakeFile, fakePage)
    assert fileHandler.sortFile() == 1
        
def test_FileHandler_video():
    fakePage = FakePage()
    fakeFile = FakeFile("video.mp4")
    fileHandler = FileHandler(fakeFile, fakePage)
    assert fileHandler.sortFile() == 2
    
def test_FileHandler_document():
    fakePage = FakePage()
    fakeFile = FakeFile("document.doc")
    fileHandler = FileHandler(fakeFile, fakePage)
    assert fileHandler.sortFile() == 3

def test_FileHandler_invalid():
    fakePage = FakePage()
    fakeFile = FakeFile("somefile")
    fileHandler = FileHandler(fakeFile, fakePage)
    assert fileHandler.sortFile() == -1