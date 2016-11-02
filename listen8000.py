import importlib
import olaf_lib
import r_local_provider_dat

from flask import Flask
from flask import request
from requests_oauthlib import OAuth2Session


app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    importlib.reload(r_local_provider_dat)

    code = request.args['code']
    state = request.args['state']
    authorization_response = 'http://localhost:8000/authorized?code=' + code + '&state=' + state
    token_url = 'http://127.0.0.1:5000/oauth/token'

    with open('r_local_provider_dat.py', 'a') as f:
        f.write('authorization_response = "' + authorization_response + '"')
        f.write('\n')
        f.write('state = "' + state + '"')
        f.write('\n')

    SESSION = OAuth2Session(r_local_provider_dat.client_id,
                            redirect_uri=olaf_lib.getRedirectURI(),
                            scope='email',
                            state=state)

    # Fetch the access token
    token = SESSION.fetch_token(token_url,
                                client_secret=r_local_provider_dat.client_secret,
                                authorization_response=authorization_response)

    with open('r_local_provider_dat.py', 'a') as f:
        f.write('token = "' + str(token) + '"')
        f.write('\n')

    # Fetch a protected resource
    SESSION = OAuth2Session(token=token)
    r = SESSION.get('http://localhost:5000/api/me',
                    cookies=dict(session=r_local_provider_dat.session_cookie)
                    )
    print(r.content)
    return(r.content)

app.debug = True
app.run(host='localhost', port=8000)
