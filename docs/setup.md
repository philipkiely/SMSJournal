## SMSJournal Setup

To set up SMSJournal, create a virtual environment and `pip install` the packages listed in "requirements.txt".

Next, ensure that you have the environment variables as described in "settings.md". Then, create a postgreSQL database with the same information as the environment variables.

Finally, cd into SMSJournal/SMSJournal (the one with "manage.py" in it) and run:

* `python manage.py migrate` (migrations are made locally and pushed with code)
* `python manage.py runserver`
