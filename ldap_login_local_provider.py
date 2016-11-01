import olaf_lib
import os
import requests
from requests_oauthlib import OAuth2Session
import sys
from bs4 import BeautifulSoup

# r = requests.get('http://127.0.0.1:5000/login')

# print(r.text)

# r = requests.get('http://127.0.0.1:5000/login')

# print(r.cookies)




# page = BeautifulSoup(r.text, 'lxml')
# txt = page.find_all('input', id='csrf_token')[0]
# print(txt['value'])

r = requests.post('http://127.0.0.1:5000/login',
                  data={'username': 'jake@acogdev.com',
                        'password': 'eagle5253'
                        }
                  )

# print(r.text)

# id_token = r.text

# r = requests.post('http://127.0.0.1:5000',
#                   data={'username': 'jake'},
#                   headers={'Authorization': id_token})

if r.status_code == 200:
    r1 = requests.get('http://127.0.0.1:5000/client',
                      cookies=r.cookies,
                      # headers={'Authorization': id_token}
                      )

    if r1.status_code == 200:
        client_dat = r1.json()
        client_id = client_dat['client_id']
        client_secret = client_dat['client_secret']

        with open('r_local_provider_dat.py', 'w') as f:
            f.write('client_id = "' + client_id + '"')
            f.write('\n')
            f.write('client_secret = "' + client_secret + '"')
            f.write('\n')
            f.write('session_cookie = "' + r1.cookies['session'] + '"')
            f.write('\n')

        authorization_base_url = 'http://127.0.0.1:5000/oauth/authorize'

        SESSION = OAuth2Session(client_id,
                                redirect_uri=olaf_lib.getRedirectURI(),
                                scope='email')

        authorization_url, state = SESSION.authorization_url(authorization_base_url)
        r = requests.post(authorization_url,
                          data={'confirauthorization_urlm': 'yes'},
                          cookies=r1.cookies)
        print(r.text)
    else:
        print('/client ' + str(r1.status_code))
else:
    print(r.status_code)

