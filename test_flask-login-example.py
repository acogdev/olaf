import os
import requests
import olaf_lib


r = requests.post('http://127.0.0.1:7000/token',
                  data={'username': 'jake', 'password': 'jake'})

token = r.text


r = requests.get('http://127.0.0.1:7000/protected/',
                 headers={'Authorization': token})

print(r.text)
