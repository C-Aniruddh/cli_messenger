import json
import requests
import time

HOST = "http://35.185.58.133/get_log"

key = str(input("Enter your key : "))
data_values = {'key' : key}

print("Sending request ...")

data_json = json.dumps(data_values)
payload = data_json

r = requests.post(HOST, json=payload)

print("Decrypting ...")

log = r.json()
print(json.dumps(log, indent=4))

