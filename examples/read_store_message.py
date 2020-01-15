import data.connection_settings as cs
import data.creds as creds
from app.messagehandler import MessageHandler

if __name__ == '__main__':
    messages = MessageHandler()
    messages.connect(cs.HOST, cs.PORT, creds.NICK, creds.OAUTH)
    messages.set_channel("#hasanabi")
    messages.get_and_store_message()
    print(messages.read_latest_message())
