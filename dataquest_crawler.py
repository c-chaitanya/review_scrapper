import requests
from requests.auth import HTTPBasicAuth
import json
r = requests.get('https://app.dataquest.io/login', auth=HTTPBasicAuth("chaitu9701@gmail.com", "Donkey09"))
resp = json.loads(r.content)
