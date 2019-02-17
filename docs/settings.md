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
