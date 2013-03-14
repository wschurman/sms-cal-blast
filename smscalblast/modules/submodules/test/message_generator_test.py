"""
Test sms.py functions with unittest.
"""

import unittest
from smscalblast.modules.submodules import *

test_events_raw = [
    {
        u'id': 1,
        u'start': {u'dateTime': u'2013-02-24T18:30:00-05:00'},
        u'end': {u'dateTime': u'2013-02-24T19:30:00-05:00'},
        u'summary': u'Chapter',
        u'description': u'#sms'
    },
    {
        u'id': 2,
        u'start': {u'dateTime': u'2013-02-24T18:30:00-05:00'},
        u'end': {u'dateTime': u'2013-02-24T19:30:00-05:00'},
        u'summary': u'Chapter',
        u'description': u'#sms #optional'
    },
    {
        u'id': 3,
        u'start': {u'dateTime': u'2013-02-24T18:30:00-05:00'},
        u'end': {u'dateTime': u'2013-02-24T19:30:00-05:00'},
        u'summary': u'Chapter',
        u'description': u'#sms #required'
    },
    {
        u'id': 4,
        u'start': {u'dateTime': u'2013-02-24T18:30:00-05:00'},
        u'end': {u'dateTime': u'2013-02-24T19:30:00-05:00'},
        u'summary': u'Chapter',
        u'description': u'blah'
    },
    {
        u'id': 5,
        u'start': {u'dateTime': u'2013-02-24T18:30:00-05:00'},
        u'end': {u'dateTime': u'2013-02-24T19:30:00-05:00'},
        u'summary': u'Chapter',
        u'description': u'#sms #specific(abc, def, ghi)'
    },
    {
        u'id': 6,
        u'start': {u'dateTime': u'2013-02-24T18:30:00-05:00'},
        u'end': {u'dateTime': u'2013-02-24T19:30:00-05:00'},
        u'summary': u'Chapter',
        u'description': u'#sms #specific(abc,def,ghi)'
    },
    {
        u'id': 7,
        u'start': {u'dateTime': u'2013-02-24T18:30:00-05:00'},
        u'end': {u'dateTime': u'2013-02-24T19:30:00-05:00'},
        u'summary': u'Chapter',
        u'description': u'#sms #specific()'
    },
    {
        u'id': 8,
        u'start': {u'dateTime': u'2013-02-24T18:30:00-05:00'},
        u'end': {u'dateTime': u'2013-02-24T19:30:00-05:00'},
        u'summary': u'Chapter',
        u'description': u'#sms #specific'
    },
    {
        u'id': 9,
        u'start': {u'dateTime': u'2013-02-24T18:30:00-05:00'},
        u'end': {u'dateTime': u'2013-02-24T19:30:00-05:00'},
        u'summary': u'Chapter',
        u'description': u'#sms #specific(blah, def)'
    }
]

test_people_raw = [
    {
        u'email': 'nospecific@blah.com',
        u'phone': '1234567899',
        u'carrier': 'verizon'
    },
    {
        u'email': 'abc@blah.com',
        u'phone': '1234567890',
        u'carrier': 'verizon'
    },
    {
        u'email': 'def@blah.com',
        u'phone': '1234567891',
        u'carrier': 'verizon'
    },
    {
        u'email': 'ghi@blah.com',
        u'phone': '1234567892',
        u'carrier': 'verizon'
    },
    {
        u'email': 'blah@blah.com',
        u'phone': '1234567892',
        u'carrier': 'verizon'
    }
]


class TestMessage(unittest.TestCase):
    pass


class TestMessageGenerator(unittest.TestCase):

    def setUp(self):
        self.test_events = [Event(e) for e in test_events_raw]
        self.test_people = [Person(p) for p in test_people_raw]

        self.message_generator = MessageGenerator(self.test_events,
                                                  self.test_people)

    def test_generate(self):
        self.assertEqual(len(self.message_generator.get_messages()), 4)
        print str(self.message_generator)

    def tearDown(self):
        self.test_events = None
        self.test_people = None
        self.message_generator = None

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMessageGenerator)
    unittest.TextTestRunner(verbosity=2).run(suite)
