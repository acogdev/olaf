import importlib
import r_local_provider_dat
from requests_oauthlib import OAuth2Session
import olaf_lib
import ast
import time


TOKEN = ''


def load_token():
    global TOKEN

    importlib.reload(r_local_provider_dat)

    try:
        TOKEN = ast.literal_eval(r_local_provider_dat.token)
    except Exception as e:
        print(e)


def test_get_data(token):
    SESSION = OAuth2Session(r_local_provider_dat.client_id,
                            redirect_uri=olaf_lib.getRedirectURI(),
                            scope='email',
                            state=r_local_provider_dat.state,
                            token=token)

    # Fetch a protected resource, i.e. user profile
    r = SESSION.get('http://localhost:5000/api/data',
                    cookies=dict(session=r_local_provider_dat.session_cookie))


def run_refresh(token):
    global TOKEN

    extra = {
        'client_id': r_local_provider_dat.client_id,
        'client_secret': r_local_provider_dat.client_secret,
    }

    SESSION = OAuth2Session(r_local_provider_dat.client_id,
                            token=token)

    refresh_url = olaf_lib.token_url
    TOKEN = SESSION.refresh_token(refresh_url, **extra)
    with open('r_local_provider_dat.py', 'a') as f:
        f.write('token = "' + str(TOKEN) + '"')
        f.write('\n')


def run_provider():
    import r_local_provider_auto


def wait(t):
    for i in range(1, t):
        print('.', end="", flush=True)
        time.sleep(1)
    print('.')


def runtest():
    run_provider()
    wait(2)
    load_token()
    test_get_data(TOKEN)

    wait(11)

    run_refresh(TOKEN)
    wait(1)
    test_get_data(TOKEN)


def test_refresh():
    load_token()

    run_refresh(TOKEN)
    wait(1)
    test_get_data(TOKEN)


if __name__ == '__main__':
    test_refresh()
