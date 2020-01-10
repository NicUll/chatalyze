import socket

from data import connection_settings as cs


class IRC(object):

    def __init__(self):
        self.socket = self.create_socket()

    def connect(self, host: str, port: int):
        self.socket.connect((host, port))

    def sendbytes(self, data: str):
        sdata = data.strip()  # Remove any extra \r, \n and other whitespace
        self.socket.send(bytes('%s\r\n' % sdata, cs.ENCODING))

    def authenticate(self, oauth, uname):
        self.sendbytes('PASS %s' % oauth)
        self.sendbytes('NICK %s' % uname)

    def join_channel(self, channel):
        self.sendbytes('JOIN %s' % channel)

    def part_channel(self, channel):
        self.sendbytes('PART %s' % channel)

    def check_ping(self, data):
        if data == cs.PING_MESSAGE:
            self.sendbytes(cs.PONG_MESSAGE)
            self.get_data()  # Risk of loop if only PING is sent
        return data

    def get_data(self) -> str:
        data = self.socket.recv(1024).decode(cs.ENCODING)
        return self.check_ping(data)

    def create_socket(self, family=socket.AF_INET, type=socket.SOCK_STREAM):  # IPv4 and TCP as standard
        return socket.socket(family, type)

