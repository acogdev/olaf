import importlib
import r_local_provider_dat
from requests_oauthlib import OAuth2Session
import olaf_lib
import ast


importlib.reload(r_local_provider_dat)

token = ast.literal_eval(r_local_provider_dat.token)

SESSION = OAuth2Session(r_local_provider_dat.client_id,
                        redirect_uri=olaf_lib.getRedirectURI(),
                        scope='email',
                        state=r_local_provider_dat.state,
                        token=token)

# Fetch a protected resource, i.e. user profile
r = SESSION.get('http://localhost:5000/api/data',
                cookies=dict(session=r_local_provider_dat.session_cookie))

print(r.content)
