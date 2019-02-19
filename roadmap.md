## SMSJournal Roadmap

### TODO: v1.0 Release

#### AWS Lambda SMS Handler
* Integrate with Django Site API
* test message parsing
* Activate Google App Script

#### Google App Script
* DONE | PK | Use POST request
* DONE | PK | Make post request to API after new journal
* Set environment variable for API api_key
* Implement login for any account
* Get published for use with any account

#### Django Site

ALL SITE TASKS MUST INCLUDE UNIT TESTS WHEREVER POSSIBLE

* DONE | PK | Project Setup
* DONE | PK | Copy over static assets
* AM | Signup/Signin with a google account
* Kuku | get phone number and verification
* get payment from stripe
* Change user's information

##### Django Site | API

ALL SITE API TASKS MUST INCLUDE UNIT TESTS WHEREVER POSSIBLE

* get journal id with phone number and lowercase journal name.
* Add new journal to user
