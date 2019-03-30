## SMSJournal Roadmap

### TODO: v1.0 Release

#### AWS Lambda SMS Handler
* Integrate with Django Site API
* test message parsing

#### Google App Script
* DONE | PK | Use POST request
* DONE | PK | Make post request to API after new journal
* Set environment variable for API api_key
* Implement login for any account
* Get published for use with any account
* PK | Integrate with Django Site API
* DONE | PK | test message parsing
* 24-hour timed analytics trigger

#### Django Site

ALL SITE TASKS MUST INCLUDE UNIT TESTS WHEREVER POSSIBLE

* DONE | PK | Project Setup
* DONE | PK | Copy over static assets
* AM | Signup/Signin with a google account
* AB | get phone number and verification
* DONE | PK | [Journal Model, API to add journal, API to get journal by name]
* Test Journals App [3 actions above]
* Add journal update to user phone number change (task below)
* /account/ page with:
    * Post an entry directly
    * change phone number with verification
    * change stripe
    * cancel subscription (refund policy? 30-day cancellation?)
* get payment from stripe


#### Business

* FAQ
    * Can I move files between folders? Yes
    * Can I change X info? Yes, here is the field
* Finish frontend
