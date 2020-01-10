import sqlite3
from typing import List


class Column:

    def __init__(self, name, data_type, properties=None):
        self.name = name
        self.data_type = data_type
        self.properties = properties

    def __str__(self):
        return "%s %s %s" % (self.name, self.data_type, self.properties)


class DBHandler:
    """
    Module for storing and getting db-values to add some abstraction
    from the database and open up for a change of db-type
    """

    def __init__(self):
        self.conn: sqlite3.Connection = None
        self.cur: sqlite3.Cursor = None

    def connect(self, database: str):
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()

    def close_connection(self):
        self.conn.close()

    def create_table(self, name: str, columns: List[Column]):
        columns_str: str = ", ".join(map(str, columns))
        statement: str = "CREATE TABLE IF NOT EXISTS %s (%s);" % (name, columns_str)
        self.cur.execute(statement)
        self.conn.commit()

    def run_sql(self, sql: str, *values):
        self.cur.execute(sql, values)
        self.conn.commit()
        return self.cur

    def run_select(self, sql: str, *values):
        return self.run_sql(sql, values).fetchall()


    def _attach_database(self, database: str, name: str):
        self.cur.execute("attach database %s as %s" % (database, name))
        self.conn.commit()

    def _detach_database(self, name: str):
        self.cur.execute("detach database %s" % name)
        self.conn.commit()

    def add_temp_db(self, name: str):
        self._attach_database(name=name)

    def remove_temp_db(self, name: str):
        self._detach_database(name=name)
