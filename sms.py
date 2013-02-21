
import re
import config
import smtplib
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
    "virgin"    :   "vmobl.com"
}


class SMS:

    def __init__(self, events, numbers):
        self.events = events
        self.numbers = self.fix_numbers(numbers)

    def fix_numbers(self, numbers):
        """
        Filters non-numrical characters out of phone numbers.
        """
        new_numbers = dict()

        for number in numbers:
            carrier = numbers[number]
            new_num = re.sub('[^0-9]+', '', number)

            if carrier in CARRIERS:
                new_numbers[new_num] = carrier

        return new_numbers

    def generate_message(self, events):
        """
        Generates the body text of the email from events.
        """
        msg_str = "Events in the next hour:\n"

        for event in events:
            if (not event['start']['dateTime'] or
               not event['end']['dateTime'] or
               not event['summary']):
               continue

            start = dateutil.parser.parse(
                        event['start']['dateTime']
                    ).astimezone(pytz.timezone('US/Eastern'))
            end   = dateutil.parser.parse(
                        event['end']['dateTime']
                    ).astimezone(pytz.timezone('US/Eastern'))

            msg_str += "%s (%s-%s)\n" % (
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

        for number in self.numbers:
            carrier = self.numbers[number]
            email_addresses.append(number + '@' + CARRIERS[carrier])

        recipients = sep.join(email_addresses)
        sender = config.cf("SMTP_SENDER")
        subject = "Required Events"
        body = self.generate_message(self.events)
        headers = ["From: " + sender,
                   "Subject: " + subject,
                   "To: " + recipients,
                   "MIME-Version: 1.0",
                   "Content-Type: text/html"]
        headers = "\r\n".join(headers)

        try:
            server, port = config.cf("SMTP_SERVER"), config.cf("SMTP_PORT")
            smtp = smtplib.SMTP(server, port)

            if config.DEBUG:
                smtp.set_debuglevel(config.DEBUG)

            smtp.sendmail(sender, recipients, headers + "\r\n\r\n" + body)
            smtp.quit()

            if config.DEBUG:
                print "SEND: " + headers + "\r\n\r\n" + body

        except Exception as e:
            if config.DEBUG:
                print e
            print "Error: unable to send email"
