import pytest
from wiki.web.reference_handler import ReferenceHandler

class FakePage:
    url = "tYYtD7HJp6"
    def __init__(self):
        pass

def test_ReferenceHandler_invalid():
    fakePage = FakePage()
    referenceHandler = ReferenceHandler("", "", "", "", "", fakePage)
    assert referenceHandler.addReference() == -1
    
def test_ReferenceHandler():
    fakePage = FakePage()
    referenceHandler = ReferenceHandler("Some Title", "", "", "", "", fakePage)
    assert referenceHandler.addReference() == "Some Title||||"