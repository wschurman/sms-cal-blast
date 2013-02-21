
import re
import smtplib

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
        new_numbers = dict()

        for number in numbers:
            carrier = numbers[number]
            new_num = re.sub('[^0-9]+', '', number)

            if carrier in CARRIERS:
                new_numbers[new_num] = carrier

        return new_numbers

    def send_messages(self):

        sep = ', '
        email_addresses = []

        for number in self.numbers:
            carrier = self.numbers[number]
            email_addresses.append(number + '@' + CARRIERS[carrier])

        recipients = sep.join(email_addresses)
        sender = "schurman@bcuccioli.com"

        subject = "test subject"
        body = "Hello, woah!"

        headers = ["From: " + sender,
                   "Subject: " + subject,
                   "To: " + recipients,
                   "MIME-Version: 1.0",
                   "Content-Type: text/html"]
        headers = "\r\n".join(headers)

        try:
            smtp = smtplib.SMTP('localhost', 1025)
            smtp.set_debuglevel(10)
            smtp.sendmail(sender, recipients, headers + "\r\n\r\n" + body)
            smtp.quit()
        except Exception as e:
            print e
            print "Error: unable to send email"
