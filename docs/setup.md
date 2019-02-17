## SMSJournal Setup

To set up an SMSJournal dev environment, create a virtual environment, activate it, then run  `pip install -r requirements.txt`.

Next, set the environment variables described in "settings.md". It may be convienent to set these variables in the activation script for your
virtual environment so that they aren't set when you aren't working on SMSJournal. This process is also described (briefly) in "settings.md".

Next, create a postgreSQL database. The name of the database should match the environment variable `SMSJOURNAL_DB_NAME` and the username and password
of a postgres user that can access the database should match the environment variables `SMSJOURNAL_DB_USER` and `SMSJOURNAL_DB_PASS`.

Finally, cd into SMSJournal/SMSJournal (the one with "manage.py" in it) and run:

* `python manage.py migrate` (migrations are made locally and pushed with code)
* `python manage.py runserver`
