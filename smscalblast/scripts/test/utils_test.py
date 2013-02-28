"""
Test utils.py functions with unittest.
"""

import unittest
from mock import MagicMock
from smscalblast.modules.test import MockSQLiteConnection
from smscalblast.scripts import utils

valid_event = {
    u'id': '12345',
    u'start': {u'dateTime': u'2013-02-24T15:00:00-05:00'},
    u'end': {u'dateTime': u'2013-02-24T16:00:00-05:00'},
    u'summary': u'Admin',
    u'description': u'#sms hello'
}

# no start
invalid_event_1 = {
    u'id': '12345',
    u'end': {u'dateTime': u'2013-02-24T19:30:00-05:00'},
    u'summary': u'Chapter',
    u'description': u'#sms'
}

# no dateTime in start
invalid_event_2 = {
    u'id': '12345',
    u'start': {u'hello': u'2013-02-24T18:30:00-05:00'},
    u'end': {u'dateTime': u'2013-02-24T19:30:00-05:00'},
    u'summary': u'Chapter',
    u'description': u'#sms'
}

# no #sms in description
invalid_event_3 = {
    u'id': '12345',
    u'start': {u'dateTime': u'2013-02-24T18:30:00-05:00'},
    u'end': {u'dateTime': u'2013-02-24T19:30:00-05:00'},
    u'summary': u'Chapter',
    u'description': u'hello world'
}

# no summary
invalid_event_4 = {
    u'id': '12345',
    u'start': {u'dateTime': u'2013-02-24T18:30:00-05:00'},
    u'end': {u'dateTime': u'2013-02-24T19:30:00-05:00'},
    u'description': u'#sms'
}

# id in DB, uses mock
invalid_event_5 = {
    u'id': '1234',
    u'start': {u'dateTime': u'2013-02-24T18:30:00-05:00'},
    u'end': {u'dateTime': u'2013-02-24T19:30:00-05:00'},
    u'summary': u'Chapter',
    u'description': u'#sms'
}


class TestUtils(unittest.TestCase):

    def setUp(self):
        pass

    def test_pick(self):
        d = {
            'hello': 'world',
            'hi': 'world',
            u'ue': 0,
            'next key': {'1': 'hello'},
            'arr': ['hello', 'world']
        }

        # all keys are valid
        valids = ['hello', 'hi', '1', u'ue', 'next key', 'arr']
        test = utils.pick(d, valids)
        self.assertDictEqual(test, d)

        # two keys are valid
        valids = ['hi', u'ue']
        test = utils.pick(d, valids)
        self.assertDictContainsSubset(test, d)
        self.assertEqual(len(test), 2)
        self.assertIn('hi', test)
        self.assertIn(u'ue', test)
        self.assertNotIn('arr', test)
        self.assertEqual(test['hi'], 'world')
        self.assertEqual(test[u'ue'], 0)
        with self.assertRaises(KeyError):
            b = test['arr']
            b.append('hi')

        # no keys are valid
        valids = []
        test = utils.pick(d, valids)
        self.assertDictContainsSubset(test, d)
        self.assertEqual(len(test), 0)

    def test_validate_event(self):
        sqlite = MockSQLiteConnection()
        self.assertTrue(utils.validate_event(sqlite, valid_event))
        self.assertFalse(utils.validate_event(sqlite, invalid_event_1))
        self.assertFalse(utils.validate_event(sqlite, invalid_event_2))
        self.assertFalse(utils.validate_event(sqlite, invalid_event_3))
        self.assertFalse(utils.validate_event(sqlite, invalid_event_4))
        sqlite.close()  # not necessary, but good to keep for compatibility

        sqlite = MockSQLiteConnection()
        sqlite.get_rows = MagicMock()
        sqlite.get_rows.return_value = [('1234')]
        self.assertFalse(utils.validate_event(sqlite, invalid_event_5))
        sqlite.get_rows.assert_called_with(
            'SELECT id FROM sent_events WHERE id = ?', ('1234',)
        )

    def tearDown(self):
        pass

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtils)
    unittest.TextTestRunner(verbosity=2).run(suite)
