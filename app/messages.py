import sqlite3


class Messages(object):

    def __init__(self):
        self.conn = sqlite3.connect('messages.db')
        self.cursor = self.conn.cursor()

    def setup_database(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='messages';")
        if not self.cursor.fetchone():
            self.cursor.execute("create table messages (data text, message text, user text, type text)")
            self.conn.commit()

    def close_connection(self):
        self.conn.close()

    def insert_message(self, message):
        pass


'''
class Message(object):

    def __init__(self, data, message="", user="", type=None):
        self.data = data
        self.message = message
        self.user = user
        self.type = type
        '''
