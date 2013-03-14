
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


class Message:
    """
    Represents a message containing a set of events
    that is sent to a set of people.
    """
    def __init__(self):
        self.people = []
        self.events = []

    def is_person_compatible(self, events):
        """
        Checks if the set of events that the person needs to be notified
        about is compatible with the set of events in this message.
        """
        if len(self.events) == 0:
            return True
        if set(events) == set(self.events):
            return True

        return False

    def add_person(self, person, events):
        """
        Adds a person after verifying validity.
        """
        if len(self.events) == 0:
            self.events = list(events)
        assert(set(events) == set(self.events))
        self.people.append(person)

    def get_addresses(self):
        """
        Generates a list of email addresses from the phone numbers.
        """
        email_addresses = []

        for person in self.people:
            carrier = person.carrier
            number = person.phone
            if carrier in CARRIERS:
                email_addresses.append(number + '@' + CARRIERS[carrier])
            else:
                email_addresses.append(person.email)

        return email_addresses

    def get_addresses_str(self):
        """
        Adds commaspace seperator to email addresses and returns a string.
        """
        addresses = self.get_addresses()
        sep = ', '

        return sep.join(addresses)

    def get_message(self):
        """
        Generate message for required and optional events.
        """
        req = [i for i in self.events if i.is_required()]
        opt = [i for i in self.events if not i.is_required()]

        msg_str = ""

        if len(req) > 0:
            msg_str = "Required Events:\r\n"
            for event in req:
                msg_str += str(event)
            if len(opt) > 0:
                msg_str += "\r\n"

        if len(opt) > 0:
            msg_str = "Optional Events:\r\n"
            for event in opt:
                msg_str += str(event)

        return msg_str.rstrip()

    def __str__(self):
        mstr = "("
        for p in self.people:
            mstr += '%s, ' % p.identifier
        mstr += ")["
        for e in self.events:
            mstr += '%s, ' % e.id
        mstr += "]"
        return mstr


class MessageGenerator:
    """
    Generates messages from a set of people and events.
    """
    def __init__(self, events, people):
        self.messages = []
        self.events = events
        self.people = people
        self.generate()

    def generate(self):
        """
        Do generation.
        """

        # dictionary from people to the events they need to be notified of
        peeps = dict()

        # add all people and add their events
        for person in self.people:
            peeps[person] = []
            for event in self.events:
                if event.contains_person(person.identifier):
                    peeps[person].append(event)

        # while we have peeps left to generate messages for
        while len(peeps) > 0:
            peep, events = peeps.popitem()

            if len(events) < 1:
                continue

            # try to add them to a existing message if they are compatible
            inserted = False
            for message in self.messages:
                if message.is_person_compatible(events):
                    message.add_person(peep, events)
                    inserted = True
                    break

            # not compatible, create a new message
            if not inserted:
                m = Message()
                m.add_person(peep, events)
                self.messages.append(m)

        # should have optimal set of messages, hopefully

    def get_messages(self):
        return self.messages

    def __str__(self):
        msg = "["
        for m in self.messages:
            msg += '%s, ' % str(m)
        msg += "]"
        return msg
