
from threading import Thread
import time

class CalThread(Thread):

    def __init__(self):
        Thread.__init__()
        self.stop = False

    def run(self):
        while not(self.stop):
            self.check_for_events()
            time.sleep(2)  # 2 seconds for now, switch to 600 for production

    def check_for_events(self):
        pass

    def send_all_sms(self):
        pass
