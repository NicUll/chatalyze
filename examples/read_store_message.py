import data.connection_settings as cs
import data.creds as creds
from app.messagehandler import MessageHandler

if __name__ == '__main__':
    messages = MessageHandler()
    messages.connect(cs.HOST, cs.PORT, creds.NICK, creds.OAUTH)
    messages.set_channel("#trainwreckstv")
    messages.store_latest(amount=30)
    stored_mes = messages.read_latest_messages(30)
    for m in stored_mes:
        print(m)
