import data.connection_settings as cs
import data.creds as creds
from app.messagehandler import MessageHandler

if __name__ == '__main__':
    messages = MessageHandler()
    messages.connect(cs.HOST, cs.PORT, creds.NICK, creds.OAUTH)
    messages.set_channel("#trainwreckstv")
    messages.store_latest(amount=2)
    print(messages.read_latest_message())
