import sqlite3
from typing import List

from app.irc import IRC


class Column:

    def __init__(self, name, data_type, properties=None):
        self.name = name
        self.data_type = data_type
        self.properties = properties

    def __str__(self):
        return "%s %s %s" % (self.name, self.data_type, self.properties)


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

    MESSAGE_TABLE = [
        Column('raw', 'text'),
        Column('user_name', 'text'),
        Column('message', 'text'),
        Column('c_time', 'text')
    ]

    USER_TABLE = [
        Column('channel_name', 'text'),
        Column('user_name', 'text'),
        Column('message_count', 'integer')
    ]

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
        self.create_table_if_empty(self.user_table, self.USER_TABLE)

    def connect(self, HOST, PORT, NICK=None, OAUTH=None):
        """
        Connects the IRC-module to host and initializes the database.

        :param HOST: IRC host-adress
        :param PORT: IRC host-port
        :param NICK: Users nickname
        :param OAUTH: Users generated oauth-value
        :return:
        """
        self._connect_irc(HOST, PORT, NICK, OAUTH)
        self._init_db()

    def set_channel(self, channel):
        """
        Part from current channel and connect to new one
        :param channel:
        :return:
        """

        if self.current_channel:
            self.irc.part_channel(self.current_channel)
        self.current_channel = channel
        self._current_message_table = 'ch_%s_messages' % self.current_channel
        self.irc.join_channel(self.current_channel)

    def run_select(self, sql: str, *values) -> List:
        result_cursor = self.conn.execute(sql, values)
        return result_cursor.fetchall()

    def store_message(self, message):
        message_data = IRC.get_message_data_dict(message)
        if message_data:
            self.conn.execute('insert into messages(message, data, user, channel) values (?,?,?,?)', message,
                              message_data['data'], message_data['user'], message_data['channel'])
        return

    def read_irc(self):
        return self.irc.get_data()

    def get_and_store_message(self):
        message = self.read_irc()
        if message:
            self.store_message(message)

    def read_latest_message(self):
        return self.read_latest_messages(1)

    def read_latest_messages(self, amount):
        return self.run_select('select * from messages limit ? order by id desc', amount)

    def create_table_if_empty(self, name: str, columns: List):
        if self.conn:
            columns_str: str = ", ".join(map(str, columns))
            statement: str = f'CREATE TABLE IF NOT EXISTS {name} ({columns_str});'
            self.conn.execute(statement)
