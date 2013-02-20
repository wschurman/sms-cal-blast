import config
from cal_thread import CalThread

import atexit
import urllib
import psutil, os, time, sys, json
from threading import Thread, Lock
from bottle import route, run, request, abort, get, post, delete, error, response

@get('/status')
def api_status():
   """
   Provides an endpoint for checking if server is up.
   Path: GET /status
   """
   response.set_header('Content-Type', 'application/json')
   return {
      'status':'online',
      'servertime':time.time(),
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
      with config.connection:
         cur = config.connection.cursor()
         ins = (r["phone"], r["provider"])
         cur.execute("INSERT INTO numbers (phone, provider) values (?, ?)", ins)

      response.status = "201 Added Number"
      response.set_header('Content-Type', 'application/json')
      return {"success":1}

@get('/')
def list_numbers():
   """
   Lists all numbers.
   Path: GET /
   """
   rows = None

   with config.connection:
      cur = config.connection.cursor()
      cur.execute("SELECT phone, provider FROM numbers")
      rows = cur.fetchall()

   response.set_header('Content-Type', 'application/json')
   return dict([ list(x) for x in rows ])


@get('/server_stats')
def get_server_stats():
   """
   Retrieves all server information.
   Path: GET /server_stats
   """
   p = psutil.Process(os.getpid())
   response.set_header('Content-Type', 'application/json')
   return {
      'status':'online',
      'servertime':time.time(),
      "num_threads":p.get_num_threads(),
      "cpu_percent":p.get_cpu_percent(interval=0),
      "memory":p.get_memory_info(),
      "connections":p.get_connections(kind='all'),
   }

@error(501)
def error501(error):
   return "API Method Not Implemented"

@error(404)
def error404(error):
   return 'Query or Method Not Found'

calthread = CalThread()
calthread.setDaemon(True)
calthread.start()

run(host=config.get("API_HOST"), port=config.get("API_PORT"))

@atexit.register
def goodbye():

   calthread.stop = True
   calthread.join()

   if config.connection:
      config.connection.close()
   print "Goodbye."