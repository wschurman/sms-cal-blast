
import sqlite3 as lite


class SQLiteConnection:
    """
    Provides SQLite connection utilities.
    """

    def __init__(self):
        self.connection = lite.connect('numbers.db')
        self.init_scripts()

    def init_scripts(self):
        """
        Initialize scripts for application.
        """
        self.execute_sql(
            "CREATE TABLE IF NOT EXISTS numbers"
            "(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
            "phone VARCHAR(20), "
            "provider VARCHAR(20))"
            , None)

        self.execute_sql(
            "CREATE TABLE IF NOT EXISTS sent_events"
            "(id TEXT NOT NULL PRIMARY KEY)"
            , None)

    def get_rows(self, sql, vals):
        """
        Runs sql with vals and returns rows.
        """
        with self.connection:
            cur = self.connection.cursor()
            if vals:
                cur.execute(sql, vals)
            else:
                cur.execute(sql)
            return cur.fetchall()

    def execute_sql(self, sql, vals):
        """
        Runs sql with vals.
        """
        with self.connection:
            cur = self.connection.cursor()
            if vals:
                cur.execute(sql, vals)
            else:
                cur.execute(sql)

    def insert_and_get_last_rowid(self, sql, vals):
        """
        Runs sql with vals and returns lastrowid.
        """
        with self.connection:
            cur = self.connection.cursor()
            if vals:
                cur.execute(sql, vals)
            else:
                cur.execute(sql)
            return cur.lastrowid

    def close(self):
        """
        Close the connection.
        """
        if self.connection:
            self.connection.close()
