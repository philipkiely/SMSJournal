## SMSJournal settings

SMSJournal uses environment variables to control the settings. The variables are as follows:

* SMSJOURNAL_SECRET_KEY="secret_key"
* SMSJOURNAL_DEBUG_INT="1" for true or "0" for false
* SMSJOURNAL_DB_NAME="db_name"
* SMSJOURNAL_DB_USER="db_user" (default: postgres)
* SMSJOURNAL_DB_PASS="db_pass" (default: postgres)
* AWS_ACCESS_KEY_ID from aws consolde IAM
* AWS_SECRET_ACCESS_KEY from aws console IAM
* AWS_PINPOINT_ID from aws pinpoint (this one is currently in settings)
* EMAIL_PASS=the info@grammiegram.com email password
* API_KEY=the api key, same as Lambda and App Script
