import sqlite3
from datetime import datetime

from app.irc import IRC


user_table = [
    Column('u_name', 'str'),
    Column('GUID', 'int')
]



class MessageHandler:
    """
    Class used to handle the messages fetched from Twitch IRC.

    The database is stored in memory as the primary goal is to work with the data in
    real-time to produce stats about the messages and channels, the messages themselves
    are then discarded as big amounts of data will be produced if enough channels are followed under
    a long time.

    Every time a new IRC-channel is chosen a table is created and stored in the _current_message_table field.
    This field should be considered private as the naming is crucial for the collection of data
    to work properly.

    User-names are stored in the user_table and the primary goal is to use this to distinguish
    between an active 'channel', and an active 'user'.

    """

    MESSAGE_TABLE = {
        'raw': {'type': 'text', 'properties': None},
        'user_name': {'type': 'text', 'properties': None},
        'message': {'type': 'text', 'properties': None},
        'c_time': {'type': 'text', 'properties': None},
    }

    USER_TABLE = {
        'channel_name': {'type': 'text', 'properties': None},
        'user_name': {'type': 'text', 'properties': None},
        'message_count':  {'type': 'integer', 'properties': None},
    }

    def __init__(self):
        self.irc: IRC = IRC()
        self.current_channel: str = ""
        self.conn: sqlite3.Connection = None
        self._database: str = ":memory:"
        self._current_message_table: str = ""
        self.user_table: str = "user"

    def _connect_irc(self, HOST, PORT, NICK, OAUTH):
        self.irc.connect(HOST, PORT)
        if NICK and OAUTH:
            self.irc.authenticate(OAUTH, NICK)

    def _init_db(self):
        self.conn = sqlite3.Connection(self._database)
        self.conn.create_table(self.user_table, user_table)

    def connect(self, HOST, PORT, NICK=None, OAUTH=None):
        self._connect_irc(HOST, PORT, NICK, OAUTH)
        self._init_db()

    def set_channel(self, channel):
        if self.current_channel:
            self.irc.part_channel(self.current_channel)
        self.current_channel = channel
        self._current_message_table = 'ch_%s_messages' % self.current_channel
        self.irc.join_channel(self.current_channel)

    def store_message(self, message):
        message_data = IRC.get_message_data_dict(message)
        if message_data:
            self.db.run_sql(f'insert into messages(message, data, user, channel) values (?,?,?,?)', message,
                            message_data['data'], message_data['user'], message_data['channel'])
        return

    def read_irc(self):
        return self.irc.get_data()

    def get_and_store_message(self):
        message = self.read_irc()
        if message:
            self.store_message()

    def read_latest_message(self):
        return self.db.run_select(f'select * from messages limit 1 order by id desc')

    def create_table_if_empty(self, name: str, columns: List):
        if self.conn:
            self.conn()



