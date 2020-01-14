import re
import socket

from data import connection_settings as cs


class IRC(object):
    """
    Class used to connect to an IRC-channel.

    Based on IRC-version IRCv3 with tag extension.
    Written to fulfill the bare-minimum to read/send messages to/from an IRC-channel
    """

    def __init__(self, encoding: str = 'UTF-8'):
        self.socket = self.create_socket()
        self.encoding: str = encoding

    def connect(self, host: str, port: int):
        """
        Connect a socket to the specified host-server

        :param host: Host-address
        :param port: Host-port to connect to
        :return:
        """
        self.socket.connect((host, port))

    def sendbytes(self, data: str):
        """
        Send a string to the channel

        Note that no syntax-testing is done on the string.

        :param data: String to send to IRC-channel.
        :return:
        """
        sdata = data.strip()  # Remove any extra \r, \n and other whitespace
        self.socket.send(bytes(f'{sdata}\r\n', self.encoding))

    def authenticate(self, oauth: str, uname: str):
        """
        Used to login to an IRC-server

        :param oauth:
        :param uname:
        :return:
        """
        self.sendbytes(f'PASS {oauth}')
        self.sendbytes(f'NICK {uname}')

    def join_channel(self, channel: str):
        """

        :param channel:
        :return:
        """
        self.sendbytes(f'JOIN {channel}')

    def part_channel(self, channel):
        self.sendbytes(f'PART {channel}')

    def check_ping(self, data):
        if data == cs.PING_MESSAGE:
            self.sendbytes(cs.PONG_MESSAGE)
            self.get_data()  # Risk of loop if only PING is sent
        return data

    def get_data(self) -> str:
        data = self.socket.recv(1024).decode(self.encoding)
        return self.check_ping(data)

    def create_socket(self, family=socket.AF_INET, type_=socket.SOCK_STREAM):  # IPv4 and TCP as standard
        return socket.socket(family, type_)


def get_message_data_dict(message: str) -> dict:
    m = re.match(fr':.*!(?P<user>[^@\s]*).*#(?P<channel>.*)\s:(?P<params>.*)', message)
    if m and len(m.groups()) == 3:
        return {'user': m.group('user'), 'channel': m.group('channel'), 'data': m.group('data')}
    return {}
