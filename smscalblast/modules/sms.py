
import time
import smtplib

from smscalblast.modules.submodules import MessageGenerator


class SMS:

    def __init__(self, config, events, people):
        self.get_config(config)
        self.events = events
        self.people = people

    def get_config(self, config):
        self.DEBUG = config.DEBUG()
        self.DEBUG_SMTP = config.DEBUG_SMTP()
        self.smtp_sender = config.cf("SMTP_SENDER")
        self.server = config.cf("SMTP_SERVER")
        self.port = config.cf("SMTP_PORT")

    def send_messages(self):
        """
        Construct and send the email.
        """
        # no people, do not email
        if len(self.people) < 1 or len(self.events) < 1:
            return

        message_generator = MessageGenerator(self.events, self.people)

        # send emails
        try:
            smtp = smtplib.SMTP(self.server, self.port)

            sent_events = []

            if self.DEBUG_SMTP:
                smtp.set_debuglevel(10)

            for message in message_generator.get_messages():
                try:
                    # create headers
                    email_addresses = message.get_addresses()
                    recipients = message.get_addresses_str()
                    sender = self.smtp_sender
                    subject = "Reminder"
                    body = message.get_message()
                    headers = ["From: " + sender,
                               "Subject: " + subject,
                               "To: " + recipients]
                    headers = "\r\n".join(headers)

                    smtp.sendmail(sender, email_addresses, headers + "\r\n\r\n" + body)

                    print ("SEND: " + time.strftime("%a, %d %b %Y %H:%M:%S") + "\r\n" +
                           headers + "\r\n\r\n" + body)

                    sent_events = sent_events + message.events

                except Exception as e:
                    if self.DEBUG:
                        print e
                    print "Error: unable to send email"

            # sent all messages
            smtp.quit()

            return list(set(sent_events))

        except Exception as e:
            if self.DEBUG:
                print e
            print "Error: unable to send email"
            return None
