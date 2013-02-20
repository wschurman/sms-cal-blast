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
config.update(config_private)

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

class SQLiteConnection:

   def __init__(self):
      self.connection = lite.connect('numbers.db')
      self.init_scripts()

   def init_scripts(self):
      self.execute_sql("CREATE TABLE IF NOT EXISTS numbers(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, phone VARCHAR(20), provider VARCHAR(20))", None)
      self.execute_sql("CREATE TABLE IF NOT EXISTS sent_events(id TEXT NOT NULL PRIMARY KEY)", None)

   def get_rows(self, sql, vals):
      with self.connection:
         cur = self.connection.cursor()
         if vals:
            cur.execute(sql, vals)
         else:
            cur.execute(sql)
         return cur.fetchall()

   def execute_sql(self, sql, vals):
      with self.connection:
         cur = self.connection.cursor()
         if vals:
            cur.execute(sql, vals)
         else:
            cur.execute(sql)

   def insert_and_get_last_rowid(self, sql, vals):
      with self.connection:
         cur = self.connection.cursor()
         if vals:
            cur.execute(sql, vals)
         else:
            cur.execute(sql)
         return cur.lastrowid

   def close(self):
      if self.connection:
         self.connection.close()
