import socket

from data import connection_settings


class IRC(object):

    def __init__(self):
        self.socket = self.create_socket()

    def connect(self, host: str, port: int):
        self.socket.connect((host, port))

    def sendbytes(self, data: str):
        self.socket.send(bytes(data, connection_settings.ENCODING))

    def authenticate(self, oauth, uname):
        self.socket.send(bytes('PASS %s\r\n' % oauth, 'UTF-8'))
        self.socket.send(bytes('NICK %s\r\n' % uname, 'UTF-8'))

    def join_channel(self, channel):
        self.socket.send(bytes('JOIN %s\r\n' % channel, 'UTF-8'))

    def part_channel(self, channel):
        self.socket.send(bytes('PART %s\r\n' % channel, 'UTF-8'))

    def get_data(self) -> str:
        data = self.socket.recv(1024).decode('UTF-8')
        return data

    def create_socket(self, family=socket.AF_INET, type=socket.SOCK_STREAM):  # IPv4 and TCP as standard
        return socket.socket(family, type)
