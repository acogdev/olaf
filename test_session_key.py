import olaf_lib
import r_local_provider_dat
from requests_oauthlib import OAuth2Session
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


token_url = 'http://127.0.0.1:5000/oauth/token'

SESSION = OAuth2Session(r_local_provider_dat.client_id,
                        redirect_uri=olaf_lib.getRedirectURI(),
                        scope='email',
                        state=r_local_provider_dat.state
                        )

# Fetch the access token
token = SESSION.fetch_token(token_url,
                            client_secret=r_local_provider_dat.client_secret,
                            authorization_response=r_local_provider_dat.authorization_response)

# Fetch a protected resource, i.e. user profile
r = SESSION.get('http://localhost:5000/api/me',
                cookies=dict(session=r_local_provider_dat.session_cookie))

print(r.content)
