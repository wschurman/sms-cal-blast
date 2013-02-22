
from modules import *

import time
from os.path import abspath, dirname
from threading import Thread

config = Config(
    cfile=dirname(abspath(__file__)) + '/config.json',
    cfile_private=dirname(abspath(__file__)) + '/config_private.json'
)

class CalThread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.stop = False

    def run(self):
        debug = config.DEBUG()

        while not(self.stop):
            if debug > 5:
                print "Checking for events"
            self.check_for_events()

            if debug > 5:
                print "Sending SMS"
            self.send_sms()

            if debug:
                time.sleep(10)
            else:
                time.sleep(600)

    def fetch_events(self):
        """
        Get events from Calendar
        """
        return Calendar(config).get_events()

    def pick(self, obj, valid_keys):
        """
        Return a copy of obj with only valid_keys.
        """
        result = {}

        for key in obj:
            if key in valid_keys:
                result[key] = obj[key]

        return result

    def check_for_events(self):
        """
        Checks for events, inserts them into 'seen' db table, constructs
        dictionary with only select keys.
        """
        events = self.fetch_events()

        if not 'items' in events:
            if config.DEBUG():
                print "No New Events"
            return

        valid_keys = ['summary', 'description', 'location', 'start', 'end']
        self.sms_items = []

        sqlite = SQLiteConnection()

        for event in events['items']:
            ins = (event['id'],)
            inserted = sqlite.insert_and_get_last_rowid(
                "INSERT OR IGNORE INTO sent_events (id) values (?)",
                ins
            )

            if inserted:  # if not duplicate
                self.sms_items.append(self.pick(event, valid_keys))

    def send_sms(self):
        """
        Gets phone numbers and sends sms messages via SMS class.
        """
        if len(self.sms_items) < 1:
            return
        sqlite = SQLiteConnection()
        rows = sqlite.get_rows("SELECT phone, provider FROM numbers", None)
        sqlite.close()

        rows = dict(rows)
        if len(rows) < 1:
            return

        SMS(config, self.sms_items, rows).send_messages()
