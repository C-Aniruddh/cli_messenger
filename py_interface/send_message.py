import json
import requests
import time

sender = "E"
message_in = str(input("Enter your message : "))
message = "%s : %s" % (sender, message_in)
key = str(input("Enter the key : "))
print("Encrypting ...")
data_values = {'key' : key, 'message' : message}
data_json = json.dumps(data_values)
payload = data_json
print("Sending ...")
r = requests.post('http://35.185.58.133/add_store_messages', json=payload)
print(r.text)
