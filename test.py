
from sms import SMS

blah = [{u'start': {u'dateTime': u'2013-02-24T18:30:00-05:00'}, u'end': {u'dateTime': u'2013-02-24T19:30:00-05:00'}, u'summary': u'Chapter'}, {u'start': {u'dateTime': u'2013-02-24T15:00:00-05:00'}, u'end': {u'dateTime': u'2013-02-24T16:00:00-05:00'}, u'summary': u'Admin'}]

smsms = SMS(blah, { '15757793474':'verizon' }).send_messages()

