import json
import os.path
import sys
import sqlite3 as lite

# load cross language config
cfile = open(os.path.dirname(__file__) + '/config.json')
config = json.load(cfile)
cfile.close()

cfile_private = open(os.path.dirname(__file__) + '/config_private.json')
config_private = json.load(cfile_private)
cfile_private.close()

# merge
config = dict(config.items() + config_private.items())

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
