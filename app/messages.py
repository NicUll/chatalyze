import re
import sqlite3

create_messages_table_query = '''
CREATE TABLE IF NOT EXISTS messages (
                                        id integer PRIMARY KEY,
                                        data text NOT NULL,
                                        message text,
                                        user text,
                                        channel text );
'''


class Messages(object):

    '''Class used to handle the messages fetched from Twitch IRC'''

    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = sqlite3.connect(self.db_file)

    def setup_database(self):
        cursor = self.connection.cursor()
        cursor.execute(create_messages_table_query)
        cursor.close()

    def close_connection(self):
        self.connection.close()

    def insert_message(self, message):
        m = re.match(r':(.*)!.*#(.*)\s:(.*)', message)
        if m and len(m.groups() == 3):
            user = m.group(1)
            channel = m.group(2)
            m_data = m.group(3)
            cursor = self.connection.cursor()
            self.cursor.execute('insert into messages(message, data, user, channel) values (?,?,?,?)', (message, m_data,
            user, channel))
        return

    def get_message(self):
        pass

