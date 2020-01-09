import re
from datetime import datetime

import app.auth as auth
from app.dbhandler import DBHandler, Column
from app.irc import IRC
from data import connection_settings as cs

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

    def __init__(self, irc):
        self.irc: IRC = irc
        self.channel: str = ""
        self.db: DBHandler = DBHandler()
        self.__database: str = ":memory:"
        self.__message_table: str = ""
        self.__user_table: str = "user"
        auth.set_credentials(auth.creds.NICK, auth.creds.OAUTH)

    def connect_irc(self, HOST, PORT):
        self.irc.connect(HOST, PORT)
        self.irc.authenticate(auth.get_credentials())

    def connect_db(self):
        self.db.connect(self.__database)
        self.create_table(self.__user_table, user_table)

    def connect(self, connection_settings):
        self.connect_irc(connection_settings.HOST, connection_settings.PORT)
        self.connect_db()

    def set_channel(self, channel: str):
        if self.channel:
            self.irc.part_channel(self.channel)
        self.channel = channel
        self.__message_table = 'ch_%s_messages' % self.channel
        self.irc.join_channel(self.channel, wait=7)

    def extract_message_data(self, message):
        m = re.match(r':.*!(?P<user>.*)#(?P<channel>.*)\s:(?P<data>.*)')


    def insert_message(self, message):
        m = re.match(r':(.*)!.*#(.*)\s:(.*)', message)
        if m and len(m.groups()) == 3:
            user = m.group(1)
            channel = m.group(2)
            m_data = m.group(3)
            cursor = self.connection.cursor()
            cursor.execute('insert into messages(message, data, user, channel) values (?,?,?,?)', (message, m_data,
                                                                                                   user, channel))
        return
