
import config
from threading import Thread
from calendar import Calendar
import time

CALENDAR_ID = config.cf("CALENDAR_ID")
SERVICE_ACCOUNT_NAME = config.cf("SERVICE_ACCOUNT_NAME")

class CalThread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.stop = False

    def run(self):
        # testing
        self.check_for_events()
        self.send_sms()
        return

        while not(self.stop):
            self.check_for_events()
            time.sleep(5)  # 2 seconds for now, switch to 600 for production

    def fetch_events(self):
        return Calendar(SERVICE_ACCOUNT_NAME, CALENDAR_ID).get_events()

    def check_for_events(self):
        events = self.fetch_events()

        if not 'items' in events:
            print "No New Events"
            return

        self.sms_items = []

        sqlite = config.SQLiteConnection()

        for event in events['items']:
            ins = (event['id'],)
            inserted = sqlite.insert_and_get_last_rowid(
                "INSERT OR IGNORE INTO sent_events (id) values (?)",
                ins
            )

            if inserted:  # if not duplicate
                self.sms_items.append(event)

            # print event['id']
            # print inserted

    def send_sms(self):
        pass
