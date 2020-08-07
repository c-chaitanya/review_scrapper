import requests
from requests.auth import HTTPBasicAuth
import json
r = requests.get('https://app.dataquest.io/login', auth=HTTPBasicAuth("", ""))
resp = json.loads(r.content)
