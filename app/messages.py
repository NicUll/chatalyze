import re
from datetime import datetime

import app.auth as auth
from app.dbhandler import DBHandler, Column
from app.irc import IRC

message_table = [
    Column('raw', str),
    Column('user', str),
    Column('message', str),
    Column('c_time', datetime),
]

user_table = [
    Column('u_name', str),
    Column('GUID', int)
]


class Messages:
    """Class used to handle the messages fetched from Twitch IRC"""

    def __init__(self):
        self.irc: IRC = IRC()
        self.channel: str = ""
        self.db: DBHandler = DBHandler()
        self.__database: str = ":memory:"
        self.__message_table: str = ""
        self.__user_table: str = "user"
        auth.set_credentials(auth.creds.NICK, auth.creds.OAUTH)

    def _connect_irc(self, HOST, PORT, NICK, OAUTH):
        self.irc.connect(HOST, PORT)
        if NICK and OAUTH:
            self.irc.authenticate(OAUTH, NICK)

    def _connect_db(self):
        self.db.connect(self.__database)
        self.db.create_table(self.__user_table, user_table)

    def connect(self, HOST, PORT, NICK=None, OAUTH=None):
        self._connect_irc(HOST, PORT, NICK, OAUTH)
        self._connect_db()

    def set_channel(self, channel):
        if self.channel:
            self.irc.part_channel(self.channel)
        self.channel = channel
        self.__message_table = 'ch_%s_messages' % self.channel
        self.irc.join_channel(self.channel)

    def store_message(self, message):
        message_data = get_message_data_dict(message)
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
        self.db.run_sql(f'select * from messages limit 1 order by id desc')




def get_message_data_dict(message):
    m = re.match(r':.*!(?P<user>.*)#(?P<channel>.*)\s:(?P<data>.*)', message)
    if m and len(m.groups() == 3):
        return {'user': m.group('user'), 'channel': m.group('channel'), 'data': m.group('data')}
    return None
