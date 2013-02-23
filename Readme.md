SMS CALENDAR BLAST
========

Blasts a set of users an SMS right before a required event.

Dependencies
============

* Python
* PIP
* SQLite3

Installation & Usage
====================

```shell
git clone git@github.com:wschurman/sms-cal-blast.git && cd sms-cal-blast && pip install -r requirements.txt
```

Setup
-----

1. Create a Google API Project and authenticate a Service Account
   [https://code.google.com/apis/console](https://code.google.com/apis/console)
2. Download the key file, and move it to the sms-cal-blast directory
3.  ```mv config_private_template.json config_private.json```
4. Fill in config_private.json with your own values.
    - DEBUG : 1 or 0
    - DEBUG_SMTP : 1 or 0, debug SMTP messages
    - API_HOST : IP address, 0.0.0.0 is localhost
    - API_PORT : port to run webserver on, must be free port
    - SMTP_SENDER : The from email address in the messages
    - SMTP_SERVER : The smtp server you would like to use
    - SMTP_PORT : The smtp port you would like to use
    - CALENDAR_ID : The Google Calendar ID, gotten from Calendar Settings page in Google Calendar
    - SERVICE_ACCOUNT_NAME : Email Address from service account in API console.
    - SERVICE_ACCOUNT_KEYFILE : The name of the service account keyfile.

```shell
python server.py
```

Contributors
=============

[William Schurman](https://github.com/wschurman)

[Bryan Cuccioli](https://github.com/bcuccioli)
