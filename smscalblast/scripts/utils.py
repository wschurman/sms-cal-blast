# Provides util functions for sms-blaster


def pick(obj, valid_keys):
    """
    Return a copy of obj with only valid_keys.
    """
    result = {}

    for key in obj:
        if key in valid_keys:
            result[key] = obj[key]

    return result


def validate_event(sqlite, event):
    """
    Validate the event fields and ensure that it has not been sent before.
    """
    try:
        ret = True
        ret &= 'id' in event
        ret &= 'start' in event
        ret &= 'end' in event
        ret &= 'dateTime' in event['start']
        ret &= 'dateTime' in event['end']
        ret &= 'summary' in event
        ret &= 'description' in event

        ret &= '#sms' in event['description']

        ins = (event['id'],)
        rows = sqlite.get_rows(
            "SELECT id FROM sent_events WHERE id = ?",
            ins
        )

        ret &= (len(rows) == 0)

        return ret

    except KeyError:
        return False


def get_phone_numbers(sqlite):
    """
    Gets the phone numbers from DB.
    """
    rows = sqlite.get_rows("SELECT phone, provider FROM numbers", None)
    return dict(rows)


def update_sent_events(sqlite, events):
    """
    Adds sent event IDs to the DB.
    """
    for event in events:
        ins = (event['id'],)
        sqlite.execute_sql(
            "INSERT OR IGNORE INTO sent_events (id) values (?)",
            ins
        )
