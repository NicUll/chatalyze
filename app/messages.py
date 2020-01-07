from app.irc import IRC


class Messages:
    """Class used to handle the messages fetched from Twitch IRC"""

    def __init__(self, irc, channel):
        self.irc: IRC = irc
        self.channel: str = channel
        self.table_name: str = 'c_%s' % channel
        self.__storage: str = ":memory:"
        self.db = object  # dbhandler

    def select_channel(self, channel: str):
        self.irc.part_channel(self.channel)
        self.channel = channel
        self.irc.join_channel(self.channel)




    '''def insert_message(self, message):
        m = re.match(r':(.*)!.*#(.*)\s:(.*)', message)
        if m and len(m.groups()) == 3:
            user = m.group(1)
            channel = m.group(2)
            m_data = m.group(3)
            cursor = self.connection.cursor()
            cursor.execute('insert into messages(message, data, user, channel) values (?,?,?,?)', (message, m_data,
                                                                                                   user, channel))
        return'''
