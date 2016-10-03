import os


def getRedirectURI():
    return 'http://localhost:8000/authorized'


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


token_url = 'http://127.0.0.1:5000/oauth/token'
