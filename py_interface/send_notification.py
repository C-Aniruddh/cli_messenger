import json
import requests
import time

HOST = "http://35.185.58.133/send"
title = str(input("Enter your title : "))
message = str(input("Enter your message : "))

data_values = {'title' : title, 'message' : message}
data_json = json.dumps(data_values)
payload = data_json
r = requests.post(HOST, json=payload)
print(r.text)
