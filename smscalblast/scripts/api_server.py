
from smscalblast.modules import *

import psutil
import os
import time
from os.path import abspath
from bottle import run, request, abort, get, post, error, response

config = Config(
    cfile=abspath('config_private.json')
)


@get('/status')
def api_status():
    """
    Provides an endpoint for checking if server is up.
    Path: GET /status
    """
    response.set_header('Content-Type', 'application/json')
    return {
        'status': 'online',
        'servertime': time.time(),
    }


@get('/hello')
def hello():
    """
    TODO: Remove
    """
    return "Hello, World!"


@post('/')
def add_number():
    """
    Adds a phone number to the db.
    Path: POST /
    """
    r = request.json
    if not r or not r["phone"] or not r["provider"]:
        abort(400, "Invalid call, bad request.")
    else:
        sqlite = SQLiteConnection()
        ins = (r["phone"], r["provider"])
        sqlite.execute_sql(
            "INSERT INTO numbers (phone, provider) values (?, ?)",
            ins
        )
        sqlite.close()

        response.status = "201 Added Number"
        response.set_header('Content-Type', 'application/json')
        return {"success": 1}


@get('/')
def list_numbers():
    """
    Lists all numbers.
    Path: GET /
    """
    ss = Spreadsheet(config)

    response.set_header('Content-Type', 'application/json')
    return ss.get_numbers()


@get('/cal')
def get_cal():
    """
    Test of the Calendar class via API.
    Path: GET /cal
    """
    response.set_header('Content-Type', 'application/json')
    return Calendar(config).get_events()


@get('/sent')
def get_sent():
    """
    List the IDs of the sent events.
    Path: GET /sent
    """
    rows = None

    sqlite = SQLiteConnection()
    rows = sqlite.get_rows("SELECT id FROM sent_events", None)
    sqlite.close()

    response.set_header('Content-Type', 'application/json')

    return {"sent": [x for x in rows]}


@get('/server_stats')
def get_server_stats():
    """
    Retrieves all server information.
    Path: GET /server_stats
    """
    p = psutil.Process(os.getpid())
    response.set_header('Content-Type', 'application/json')
    return {
        'status': 'online',
        'servertime': time.time(),
        "num_threads": p.get_num_threads(),
        "cpu_percent": p.get_cpu_percent(interval=0),
        "memory": p.get_memory_info(),
        "connections": p.get_connections(kind='all'),
    }


@error(501)
def error501(error):
    return "API Method Not Implemented"


@error(404)
def error404(error):
    return 'Query or Method Not Found'


def main():
    run(host=config.get("API_HOST"), port=config.get("API_PORT"))

if __name__ == '__main__':
    main()
