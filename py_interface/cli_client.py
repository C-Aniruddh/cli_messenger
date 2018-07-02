#! /usr/bin/env python

import json
import requests
import time

sender = "E"
choice = 0
HOST = "http://encmsgapi.ml"

def get_log():
    endpoint = "%s/get_log" % HOST
    key = str(input("Enter your key : "))
    data_values = {'key' : key}
    print("Sending request ...")
    data_json = json.dumps(data_values)
    payload = data_json
    r = requests.post(endpoint, json=payload)
    print("Decrypting ...")
    log = r.json()
    print(json.dumps(log, indent=4))

def send_message():
    endpoint = "%s/add_store_messages" % (HOST)
    message_in = str(input("Enter your message : "))
    message = "%s : %s" % (sender, message_in)
    key = str(input("Enter the key : "))
    print("Encrypting ...")
    data_values = {'key' : key, 'message' : message}
    data_json = json.dumps(data_values)
    payload = data_json
    print("Sending ...")
    r = requests.post(endpoint, json=payload)
    print(r.text)

def send_notification():
    endpoint = "%s/send" % (HOST)
    title = str(input("Enter your title : "))
    message = str(input("Enter your message : "))
    data_values = {'title' : title, 'message' : message}
    data_json = json.dumps(data_values)
    payload = data_json
    r = requests.post(endpoint, json=payload)
    print(r.text)

while(choice != 99):
    print("\t-- 1. Send notification")
    print("\t-- 2. Send message")
    print("\t-- 3. Get log")
    print("\t-- 99. Exit")
    choice = int(input("Enter your choice : "))
    if(choice == 1):
        send_notification()
    elif (choice == 2):
        send_message()
    elif (choice == 3):
        get_log()
    elif (choice == 99):
        pass
