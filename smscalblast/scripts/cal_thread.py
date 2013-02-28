
from smscalblast.modules import *
import utils

import time
from os.path import abspath
from threading import Thread

config = Config(
    cfile=abspath('config_private.json')
)


class CalThread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.stop = False
        self.sms_items = []
        self.DEBUG = config.DEBUG()

    def run(self):
        while not(self.stop):
            self.check_for_events()
            self.send_sms()
            time.sleep(30)
        return

    def check_for_events(self):
        """
        Checks for events, inserts them into 'seen' db table, constructs
        dictionary with only select keys.
        """
        if self.DEBUG:
            print "Checking for events"

        events = Calendar(config).get_events()

        if not 'items' in events:
            if self.DEBUG:
                print "No Events Returned"
            return

        valid_keys = ['summary', 'description', 'location', 'start', 'end', 'id']
        self.sms_items = []

        sqlite = SQLiteConnection()

        for event in events['items']:
            if utils.validate_event(sqlite, event):
                self.sms_items.append(utils.pick(event, valid_keys))

        sqlite.close()

    def send_sms(self):
        """
        Gets phone numbers and sends sms messages via SMS class.
        """
        if self.DEBUG:
            print "Sending SMS"

        # no items to send
        if len(self.sms_items) < 1:
            if self.DEBUG:
                print "No events to send"
            return

        sqlite = SQLiteConnection()
        numbers = utils.get_phone_numbers(sqlite)
        sqlite.close()

        # no phone numbers
        if len(numbers) < 1:
            if debug:
                print "No numbers to send to"
            return

        # send events
        sent_events = SMS(config, self.sms_items, numbers).send_messages()

        # update DB
        sqlite = SQLiteConnection()
        utils.update_sent_events(sqlite, sent_events)
        sqlite.close()
