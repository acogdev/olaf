import os


def getRedirectURI():
    return 'http://localhost:8000/authorized'


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
