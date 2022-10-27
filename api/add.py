import re
from urllib import response
import requests
import json

URL = 'http://127.0.0.1:8000/add/'
data = {"name":'ciao'}

response = requests.post(url=URL, json=data)

print(response.text)