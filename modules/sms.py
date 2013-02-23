
import re, time, smtplib
from datetime import timedelta, datetime
import dateutil.parser
import pytz

CARRIERS = {
    "alltel"    :   "text.wireless.alltel.com",
    "att"       :   "txt.att.net",
    "nextel"    :   "messaging.nextel.com",
    "sprint"    :   "messaging.sprintpcs.com",
    "tmobile"   :   "tmomail.net",
    "uscellular":   "email.uscc.net",
    "verizon"   :   "vtext.com",
    "virgin"    :   "vmobl.com",
    "email"     :   ""
}


class SMS:

    def __init__(self, config, events, numbers):
        self.get_config(config)
        self.events = events
        self.numbers = self.fix_numbers(numbers)

    def get_config(self, config):
        self.DEBUG = config.DEBUG()
        self.DEBUG_SMTP = config.DEBUG_SMTP()
        self.smtp_sender = config.cf("SMTP_SENDER")
        self.server = config.cf("SMTP_SERVER")
        self.port = config.cf("SMTP_PORT")

    def fix_numbers(self, numbers):
        """
        Filters non-numrical characters out of phone numbers.
        """
        new_numbers = dict()

        for number in numbers:
            carrier = numbers[number]
            new_num = re.sub('[^0-9]+', '', number)

            # remove 1
            if len(new_num) > 10 and new_num[0] == '1':
                new_num = new_num[1:]

            if carrier in CARRIERS:
                new_numbers[new_num] = carrier

        return new_numbers

    def generate_message(self, events):
        """
        Generates the body text of the email from events.
        """
        msg_str = "Required Events:\r\n"

        for event in events:
            start = dateutil.parser.parse(
                        event['start']['dateTime']
                    ).astimezone(pytz.timezone('US/Eastern'))
            end   = dateutil.parser.parse(
                        event['end']['dateTime']
                    ).astimezone(pytz.timezone('US/Eastern'))

            msg_str += "%s (%s-%s)\r\n" % (
                event['summary'],
                start.strftime("%I:%M%p"),
                end.strftime("%I:%M%p")
            )

        return msg_str.rstrip()

    def send_messages(self):
        """
        Construct and send the email.
        """
        sep = ', '
        email_addresses = []

        # no numbers, do not email
        if len(self.numbers) < 1:
            return

        # convert to email addresses via carrier SMS email addresses
        for number in self.numbers:
            carrier = self.numbers[number]
            if CARRIERS[carrier]:
                email_addresses.append(number + '@' + CARRIERS[carrier])
            else:
                email_addresses.append(number)

        # create headers
        recipients = sep.join(email_addresses)
        sender = self.smtp_sender
        subject = "Reminder"
        body = self.generate_message(self.events)
        headers = ["From: " + sender,
                   "Subject: " + subject,
                   "To: " + recipients]
        headers = "\r\n".join(headers)

        # send emails
        try:
            smtp = smtplib.SMTP(self.server, self.port)

            if self.DEBUG_SMTP:
                smtp.set_debuglevel(10)

            smtp.sendmail(sender, email_addresses, headers + "\r\n\r\n" + body)
            smtp.quit()

            print ("SEND: " + time.strftime("%a, %d %b %Y %H:%M:%S") + "\r\n" +
                    headers + "\r\n\r\n" + body)
            return self.events

        except Exception as e:
            if self.DEBUG:
                print e
            print "Error: unable to send email"
            return None
