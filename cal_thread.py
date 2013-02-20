
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
        print self.check_for_events()
        return

        while not(self.stop):
            self.check_for_events()
            time.sleep(5)  # 2 seconds for now, switch to 600 for production

    def check_for_events(self):
        cal = Calendar(SERVICE_ACCOUNT_NAME, CALENDAR_ID)
        return cal.get_events()

    def send_all_sms(self):
        pass
