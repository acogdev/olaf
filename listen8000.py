import os
import importlib
import r_local_provider_dat
from requests_oauthlib import OAuth2Session
from flask import Flask
from flask import request
app = Flask(__name__)

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


def getRedirectURI():
    return 'http://localhost:8000/authorized'


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # Get the authorization verifier code from the callback url
    # authorization_response = input('Paste the full redirect URL here:')
    importlib.reload(r_local_provider_dat)

    code = request.args['code']
    state = request.args['state']
    authorization_response = 'http://localhost:8000/authorized?code=' + code + '&state=' + state
    token_url = 'http://127.0.0.1:5000/oauth/token'

    with open('r_local_provider_dat.py', 'a') as f:
        f.write('\n')
        f.write('authorization_response = "' + authorization_response + '"')
        f.write('\n')
        f.write('state = "' + state + '"')

    SESSION = OAuth2Session(r_local_provider_dat.client_id,
                            redirect_uri=getRedirectURI(),
                            scope='email',
                            state=state)

    # Fetch the access token
    token = SESSION.fetch_token(token_url,
                                client_secret=r_local_provider_dat.client_secret,
                                authorization_response=authorization_response)

    # Fetch a protected resource, i.e. user profile
    r = SESSION.get('http://localhost:5000/api/me',
                    cookies=dict(session=r_local_provider_dat.session_cookie))
    print(r.content)
    return(r.content)

app.debug = True
app.run(host='localhost', port=8000)
