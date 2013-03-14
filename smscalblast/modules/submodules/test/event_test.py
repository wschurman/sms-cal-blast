"""
Test event.py functions with unittest.
"""

import unittest
from smscalblast.modules.submodules import Event

test_events = [
    {
        u'start': {u'dateTime': u'2013-02-24T18:30:00-05:00'},
        u'end': {u'dateTime': u'2013-02-24T19:30:00-05:00'},
        u'summary': u'Chapter',
        u'description': u'#sms'
    },
    {
        u'start': {u'dateTime': u'2013-02-24T18:30:00-05:00'},
        u'end': {u'dateTime': u'2013-02-24T19:30:00-05:00'},
        u'summary': u'Chapter',
        u'description': u'#sms #optional'
    },
    {
        u'start': {u'dateTime': u'2013-02-24T18:30:00-05:00'},
        u'end': {u'dateTime': u'2013-02-24T19:30:00-05:00'},
        u'summary': u'Chapter',
        u'description': u'#sms #required'
    },
    {
        u'start': {u'dateTime': u'2013-02-24T18:30:00-05:00'},
        u'end': {u'dateTime': u'2013-02-24T19:30:00-05:00'},
        u'summary': u'Chapter',
        u'description': u'blah'
    },
    {
        u'start': {u'dateTime': u'2013-02-24T18:30:00-05:00'},
        u'end': {u'dateTime': u'2013-02-24T19:30:00-05:00'},
        u'summary': u'Chapter',
        u'description': u'#sms #specific(abc, def, ghi)'
    },
    {
        u'start': {u'dateTime': u'2013-02-24T18:30:00-05:00'},
        u'end': {u'dateTime': u'2013-02-24T19:30:00-05:00'},
        u'summary': u'Chapter',
        u'description': u'#sms #specific(abc,def,ghi)'
    },
    {
        u'start': {u'dateTime': u'2013-02-24T18:30:00-05:00'},
        u'end': {u'dateTime': u'2013-02-24T19:30:00-05:00'},
        u'summary': u'Chapter',
        u'description': u'#sms #specific()'
    },
    {
        u'start': {u'dateTime': u'2013-02-24T18:30:00-05:00'},
        u'end': {u'dateTime': u'2013-02-24T19:30:00-05:00'},
        u'summary': u'Chapter',
        u'description': u'#sms #specific'
    }
]


class TestEvent(unittest.TestCase):

    def setUp(self):
        self.events = []
        for i in test_events:
            self.events.append(Event(i))

    def test_tags(self):
        for e in self.events:
            self.assertIn('#optional', e.tags)
            self.assertIn('#specific', e.tags)
            self.assertNotIn('#sms', e.tags)
            self.assertEqual(len(e.tags), 2)

    def test_get_specific_people(self):
        for e in self.events[5:8]:
            self.assertTrue(e.tags.get('#specific'))

        self.assertListEqual(
            self.events[4].specific_people, ['abc', 'def', 'ghi'])
        self.assertListEqual(
            self.events[5].specific_people, ['abc', 'def', 'ghi'])
        self.assertListEqual(self.events[6].specific_people, [])
        self.assertListEqual(self.events[7].specific_people, [])

    def test_is_required(self):
        self.assertTrue(self.events[0].is_required())
        self.assertFalse(self.events[1].is_required())

    def test_contains_person(self):
        self.assertTrue(self.events[0].contains_person('haha'))
        self.assertTrue(self.events[1].contains_person('what'))
        self.assertTrue(self.events[2].contains_person('hello'))
        self.assertTrue(self.events[3].contains_person('ohai'))

        self.assertTrue(self.events[4].contains_person('abc'))
        self.assertFalse(self.events[4].contains_person('blah'))

        self.assertTrue(self.events[5].contains_person('abc'))
        self.assertFalse(self.events[5].contains_person('lkj'))

        self.assertFalse(self.events[6].contains_person(''))
        self.assertFalse(self.events[7].contains_person(''))

    def tearDown(self):
        self.events = []

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEvent)
    unittest.TextTestRunner(verbosity=2).run(suite)
