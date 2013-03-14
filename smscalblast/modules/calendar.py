
import httplib2
from datetime import timedelta, datetime
import pytz

from smscalblast.scripts import utils
from smscalblast.modules.submodules import Event
from smscalblast.modules.submodules import SQLiteConnection

from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials


class Calendar:

    def __init__(self, config):
        self.get_config(config)
        self.authenticate_service()

    def get_config(self, config):
        self.DEBUG = config.DEBUG()
        self.keyfile = config.cf("SERVICE_ACCOUNT_KEYFILE")
        self.service_account_name = config.cf("SERVICE_ACCOUNT_NAME")
        self.calendarId = config.cf("CALENDAR_ID")

    def authenticate_service(self):
        """
        Authenticate with Google APIs using Google Service Accounts.
        """
        f = open(self.keyfile, "rb")
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
        """
        Fetch events via API call.
        """
        mintime = datetime.now(pytz.timezone('US/Eastern'))
        maxtime = mintime + timedelta(hours=1)

        raw_events = self.service.events().list(
            calendarId=self.calendarId,
            singleEvents=True,
            timeMin=mintime.isoformat(),
            timeMax=maxtime.isoformat(),
            orderBy="startTime"
        ).execute(http=self.http)

        if not 'items' in raw_events:
            if self.DEBUG:
                print "No Events Returned"
            return []

        events = []
        sqlite = SQLiteConnection()

        for event in raw_events['items']:
            if utils.validate_event(sqlite, event):
                events.append(Event(event))

        for e in events:
            print e.debug_str()

        sqlite.close()

        return events
