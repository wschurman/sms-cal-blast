

class Person:
    """
    Represents a person with a email, phone number, and carrier.
    """
    def __init__(self, raw_dict):
        self.email = raw_dict.get('email')
        self.phone = raw_dict.get('phone')
        self.carrier = raw_dict.get('carrier')

        self.identifier = self.email.partition('@')[0]

    def __str__(self):
        return "%s: %s, %s" % (self.identifier, self.phone, self.carrier)
