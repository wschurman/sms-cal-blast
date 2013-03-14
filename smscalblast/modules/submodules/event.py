
import dateutil.parser
import pytz

TAGS = {
    "#optional": False,
    "#specific": False
}


class Event:
    """
    Represents an event from the calendar.
    """
    def __init__(self, raw_event):
        self.raw_event = raw_event
        self.tags = dict(TAGS)

        self.parse(raw_event)

        self.specific_people = []
        self.parse_tags()

    def __hash__(self):
        assert(self.id is not None)
        return hash(self.id)

    def parse(self, raw_event):
        """
        Parses the raw_event dictionary into fields.
        """
        self.id = raw_event.get('id')
        self.name = raw_event.get('summary')
        self.description = raw_event.get('description')
        self.location = raw_event.get('location')

        self.start = dateutil.parser.parse(
            self.raw_event['start']['dateTime']
        ).astimezone(pytz.timezone('US/Eastern'))
        self.end = dateutil.parser.parse(
            self.raw_event['end']['dateTime']
        ).astimezone(pytz.timezone('US/Eastern'))

    def parse_tags(self):
        """
        Parse # tags in description used for targeted sms sending.
        """
        for tag in self.tags:
            self.tags[tag] = (tag in self.description)

        if self.tags["#specific"]:
            self.specific_people = self.get_specific_people()

    def get_specific_people(self):
        """
        Parse people listed in parentheses:
        #specific(person1, person2, person3)
        """
        pos = self.description.find("#specific")
        l_paren = self.description.find('(', pos + 8)  # magic number...
        r_paren = self.description.find(')', l_paren)
        if l_paren == -1 or r_paren == -1:
            return []

        p_str = self.description[l_paren + 1:r_paren]
        if not p_str:
            return []
        p_str = p_str.replace(" ", "")
        peeps = p_str.split(',')
        return peeps

    def is_required(self):
        """
        Check whether the event is required.
        """
        return not self.tags.get("#optional")

    def contains_person(self, identifier):
        """
        Does the event affect the person identified.
        """
        if not self.tags["#specific"]:
            return True
        else:
            return (identifier in self.specific_people)

    def debug_str(self):
        """
        Debug representation of Event.
        """
        return "%s (%s)" % (self.name, ", ".join(self.get_specific_people()))

    def __str__(self):
        """
        String representation of the event, used for message content.
        """
        return "%s (%s-%s)\r\n" % (
            self.name,
            self.start.strftime("%I:%M%p"),
            self.end.strftime("%I:%M%p")
        )
