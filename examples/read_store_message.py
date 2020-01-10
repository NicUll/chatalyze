from app.messages import Messages
import data.connection_settings as cs
import data.creds as creds

messages = Messages()
messages.connect(cs.HOST, cs.PORT, creds.NICK, creds.OAUTH)
messages.set_channel("#hasanabi")

