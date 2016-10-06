import os
import requests
import olaf_lib



r1 = requests.get('http://127.0.0.1:7000/protected/',
                   headers = {'Authorization': 'JohnDoe:John'})

print(r1.text)
