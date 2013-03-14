# Mocks the SQLite connection class


class MockSQLiteConnection():
    """
    Provides SQLite connection utilities.
    """

    def __init__(self):
        self.connection = None
        self.init_scripts()

    def init_scripts(self):
        """
        Initialize scripts for application.
        """
        return True

    def get_rows(self, sql, vals):
        """
        Runs sql with vals and returns rows.
        """
        return []

    def execute_sql(self, sql, vals):
        """
        Runs sql with vals.
        """
        return True

    def insert_and_get_last_rowid(self, sql, vals):
        """
        Runs sql with vals and returns lastrowid.
        """
        return 0

    def close(self):
        """
        Close the connection.
        """
        return True
