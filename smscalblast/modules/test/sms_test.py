"""
Test sms.py functions with unittest.
"""

import unittest
from smscalblast.modules import SMS, Config
from os.path import dirname, abspath


test_config = Config(dirname(abspath(__file__)) + '/test_config.json')

test_events = [
    {
        u'start': {u'dateTime': u'2013-02-24T15:00:00-05:00'},
        u'end': {u'dateTime': u'2013-02-24T16:00:00-05:00'},
        u'summary': u'Admin',
        u'description': u'#sms'
    },
    {
        u'start': {u'dateTime': u'2013-02-24T18:30:00-05:00'},
        u'end': {u'dateTime': u'2013-02-24T19:30:00-05:00'},
        u'summary': u'Chapter',
        u'description': u'#sms'
    }
]

test_numbers = {
    '5757493374': 'verizon',
    '1 (201) 754-8227': 'att',
    '12044560284': 'tmobile',
    '111': 'verizon'
}

test_message = u'Required Events:\r\nAdmin (03:00PM-04:00PM)' \
                '\r\nChapter (06:30PM-07:30PM)'


class TestSMS(unittest.TestCase):

    def setUp(self):
        self.sms = SMS(test_config, test_events, test_numbers)

    def test_fix_numbers(self):
        fixed_numbers = self.sms.numbers

        self.assertIn('5757493374', fixed_numbers)

        self.assertNotIn('1 (201) 754-8227', fixed_numbers)
        self.assertNotIn('12017548227', fixed_numbers)
        self.assertIn('2017548227', fixed_numbers)

        self.assertNotIn('12044560284', fixed_numbers)
        self.assertIn('2044560284', fixed_numbers)

        self.assertEqual(len(fixed_numbers), 3)

    def test_generate_message(self):
        message = self.sms.generate_message()
        self.assertEqual(message, test_message)

    def tearDown(self):
        self.sms = None

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSMS)
    unittest.TextTestRunner(verbosity=2).run(suite)
