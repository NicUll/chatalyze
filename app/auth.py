import data.creds as creds

__OAUTH = None
__NICK = None

def get_credentials():
    return (__OAUTH, __NICK)
    # TODO create full auth-module

def set_credentials(oauth, nick):
    __OAUTH = oauth
    __NICK = nick
