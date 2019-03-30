## SMSJournal settings

SMSJournal uses environment variables to control the settings. The variables are as follows:

* SMSJOURNAL_SECRET_KEY="secret_key"
* SMSJOURNAL_DEBUG_INT="1" for true or "0" for false
* SMSJOURNAL_DB_NAME="db_name"
* SMSJOURNAL_DB_USER="db_user" (default: postgres)
* SMSJOURNAL_DB_PASS="db_pass" (default: postgres)

It is convienent to set these environment variables in your virtual environment scripts so that they aren't sitting around when the project isn't being worked on.

For the activation script, add the following lines:

On POSIX systems:
```
export SMSJOURNAL_SECRET_KEY="secret_key"
export SMSJOURNAL_DEBUG_INT="debug_num"
export SMSJOURNAL_DB_NAME="db_name"
export SMSJOURNAL_DB_USER="db_user"
export SMSJOURNAL_DB_PASS="db_pass"
```

On Windows systems:
```
set "SMSJOURNAL_SECRET_KEY=secret_key"
set "SMSJOURNAL_DEBUG_INT=debug_num"
set "SMSJOURNAL_DB_NAME=db_name"
set "SMSJOURNAL_DB_USER=db_user"
set "SMSJOURNAL_DB_PASS=db_pass"
```

For the deactivation, add the following lines

On POSIX systems (add this to the deactivation section of the `activate` script):
```
unset SMSJOURNAL_SECRET_KEY
unset SMSJOURNAL_DEBUG_INT
unset SMSJOURNAL_DB_NAME
unset SMSJOURNAL_DB_USER
unset SMSJOURNAL_DB_PASS
```

On Windows systems (add this to the `deactivate.bat` script):
```
set SMSJOURNAL_SECRET_KEY=
set SMSJOURNAL_DEBUG_INT=
set SMSJOURNAL_DB_NAME=
set SMSJOURNAL_DB_USER=
set SMSJOURNAL_DB_PASS=
```

It might be wise to wrap the unsetting lines in appropriate IF blocks as follows to keep everything working if they weren't set properly:

On POSIX systems:
```
if ! [ -z "${VARIABLE_NAME+_}" ] ; then
    unset VARIABLE_NAME
fi
```

On Windows sytems:
```
if not defined VARIABLE_NAME goto ENDIFVARNAME
    set VARIABLE_NAME=
:ENDIFVARNAME
```
* SMSJOURNAL_OAUTH2_KEY="Google OAuth ClientId"
* SMSJOURNAL_OAUTH2_SECRET="Google OAuth ClientSecret"
* EMAIL_PASS=the info@grammiegram.com email password
* API_KEY=the api key, same as Lambda and App Script # TODO test and prod api keys

For information about what you need for OAuth2 with Google, [read this.](https://developers.google.com/identity/protocols/OAuth2?csw=1)

If you plan on deploying to AWS from your dev environment, you'll need these additional environment variables:

* AWS_ACCESS_KEY_ID from aws consode IAM
* AWS_SECRET_ACCESS_KEY from aws console IAM
* AWS_PINPOINT_ID from aws pinpoint (this one is currently in settings)

As an alternative to setting the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables, you can
use a credentials file [as described here.](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)
This is very useful if you have credentials for [multiple different AWS accounts.](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html)
If you don't use a credentials file, [you should read this.](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html)
