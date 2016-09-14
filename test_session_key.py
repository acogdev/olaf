import os
import requests
from requests_oauthlib import OAuth2Session
import olaf_lib
import r_local_provider_dat

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


client_id = r_local_provider_dat.client_id
client_secret = r_local_provider_dat.client_secret

authorization_base_url = 'http://127.0.0.1:5000/oauth/authorize'
token_url = 'http://127.0.0.1:5000/oauth/token'

SESSION = OAuth2Session(client_id,
                        redirect_uri=olaf_lib.getRedirectURI(),
                        scope='email')

# Redirect user to GitHub for authorization
authorization_url, state = SESSION.authorization_url(authorization_base_url)

r = requests.post(authorization_url,
                  data={'confirm': 'yes'},
                  cookies=dict(session=r_local_provider_dat.session_cookie))
