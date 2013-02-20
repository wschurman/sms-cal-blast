import json
import os.path
import sys
import sqlite3 as lite

# load cross language config
cfile = open(os.path.dirname(__file__) + '/config.json')
config = json.load(cfile)
cfile.close()

def cf(key):
   """
   Gets a config value, removes unicode if necessary.
   """
   if isinstance(config[key], int):
      return config[key]
   else:
      return str(config[key])

def get(key):
   return cf(key)


# Connect to SQLite

connection = lite.connect('numbers.db')

with connection:
   cur = connection.cursor()
   cur.execute("CREATE TABLE IF NOT EXISTS numbers(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, phone VARCHAR(20), provider VARCHAR(20))")
