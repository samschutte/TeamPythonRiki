FYI - 
 tests has its own config.py, content folder and user folder!!!
 > THE CONFIG FILE MUST BE SET UP BEFORE IT CAN BE USED


TO RUN TESTS YOU MUST FIRST:
> copy tests/config.py.template into a new file tests/config.py
> change tets/config.py to point to tests/content and tests/user
   (I know this is a pain, but I didn't find a better way)

> pip install -r requirements.txt       or      pip install pytest
    #note requirements has been updated to include pytest


Then the testing suite can be run with the command from the Riki Directory:
> pytest 