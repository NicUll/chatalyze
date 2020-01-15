import re
import sqlite3
from datetime import datetime
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
        Column('user_name', 'text'),
        Column('message', 'text'),
        Column('type', 'text'),
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
        self._current_message_table = f'ch_{channel.replace("#", "")}_messages'
        self.irc.join_channel(channel)
        self.create_table_if_empty(self._current_message_table, self.MESSAGE_TABLE)
        self.current_channel = channel

    def read_irc(self):
        return self.irc.get_data()

    def run_select(self, sql: str, *values) -> List:
        result_cursor = self.conn.execute(sql, values)
        return result_cursor.fetchall()

    def store_message_data(self, message_data: dict):
        """
        Store private message in the corresponding channel-table.

        Store user, channel and the actual message in separate columns together with
        the raw original message.

        :param message_data: The message-data dict retrieved from IRC
        :return:
        """

        self.conn.execute(
            f'insert into {self._current_message_table}(user_name, message, c_time) values (?,?,?,?)', (
                message_data['user'], message_data['data'], datetime.now()))
        print(self.run_select(f'select * from {self._current_message_table}'))

    def store_latest(self, amount=1, cmd=[]):
        handled_messages = 0
        while handled_messages < amount:

            irc_data = self.read_irc()
            messages = re.split(r'\r\n', irc_data)
            messages.pop()

            for message in messages:
                if cmd and IRC.get_message_command(message) not in cmd:
                    continue

                data = IRC.get_message_data_dict(message)
                if not data:
                    continue

                self.store_message_data(data)
                handled_messages += 1

                if handled_messages >= amount:
                    break

    def read_latest_messages(self, amount):
        return self.run_select(f'select * from {self._current_message_table} limit ? order by ROWID desc', amount)

    def read_latest_message(self):
        return self.read_latest_messages(1)

    def create_table_if_empty(self, name: str, columns: List):
        if self.conn:
            columns_str: str = ", ".join(map(str, columns))
            statement: str = f'CREATE TABLE IF NOT EXISTS {name} ({columns_str});'
            self.conn.execute(statement)
