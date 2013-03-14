
from smscalblast.modules import *
from smscalblast.modules.submodules import *
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
        self.events = []
        self.DEBUG = config.DEBUG()

    def run(self):
        while not(self.stop):
            self.do_check()
            time.sleep(30)
        return

    def do_check(self):
        """
        Gets phone numbers and sends sms messages via SMS class.
        """
        if self.DEBUG:
            print "Checking for events"

        self.events = Calendar(config).get_events()

        # no items to send
        if len(self.events) < 1:
            if self.DEBUG:
                print "No events to send"
            return

        if self.DEBUG:
            print "Sending SMS"

        people = Spreadsheet(config).get_people()

        # no phone numbers
        if len(people) < 1:
            if debug:
                print "No numbers to send to"
            return

        # send events
        sent_events = SMS(config, self.events, people).send_messages()

        # update DB
        sqlite = SQLiteConnection()
        utils.update_sent_events(sqlite, sent_events)
        sqlite.close()
