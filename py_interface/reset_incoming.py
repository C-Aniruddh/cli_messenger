import requests

r = requests.get('http://35.185.58.133/reset_incoming')
print(r.text)
