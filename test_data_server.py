import requests
import r_local_provider_dat


r = requests.get('http://localhost:8080', headers={'token': r_local_provider_dat.token})

print(r.status_code)
print(r.text)
