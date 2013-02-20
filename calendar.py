
import httplib2
from datetime import timedelta, datetime
import pytz

from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials


class Calendar:

    def __init__(self, service_acct_name, cal_id):
        self.service_account_name = service_acct_name
        self.calendarId = cal_id
        self.authenticate_service()

    def authenticate_service(self):
        f = open("key.p12", "rb")
        key = f.read()
        f.close()

        credentials = SignedJwtAssertionCredentials(
            service_account_name=self.service_account_name,
            private_key=key,
            scope='https://www.googleapis.com/auth/calendar.readonly',
        )

        self.http = httplib2.Http()
        self.http = credentials.authorize(self.http)

        self.service = build('calendar', 'v3', http=self.http)

    def get_events(self):

        mintime = datetime.now(pytz.timezone('US/Eastern'))
        maxtime = mintime + timedelta(days=10)  # debug, def. hours=1

        events = self.service.events().list(
            calendarId=self.calendarId,
            singleEvents=True,
            timeMin=mintime.isoformat(),
            timeMax=maxtime.isoformat()
        ).execute(http=self.http)

        return events
