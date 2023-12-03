FYI - 
 tests has its own config.py, content folder and user folder!!!
 > THE CONFIG FILE MUST BE SET UP BEFORE IT CAN BE USED


TO RUN TESTS YOU MUST FIRST:
> copy tests/config.py.template into a new file tests/config.py
> change tets/config.py to point to tests/content and tests/user

> pip install -r requirements.txt       or      pip install pytest
    #requirements has been updated to include pytest


Then the testing suite can be run with the command from the Riki Directory:
> pytest 

Regression Testing: All unittests are run at the same time to ensure new unittests do not effect previous testing. 
This is implemeneted automatically by running 'pytest' from the Riki directory. 

Integration Testing: All integration test files include the name of the feature and Integration to differentiate between unit test files and Integration

Acceptance Testing: A seperate directory for Acceptance can be found in tests directoy. This contains a .side file that can be opened and run
through Selenium IDE with chrome extension.
        # Setting "Allow file url" needs to be toggled on for upload file test to work correctly