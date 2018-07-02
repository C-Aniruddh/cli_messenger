from flask import Flask, render_template, url_for, request, session, redirect, send_from_directory, jsonify
import base64
import json
import requests
from flask_pymongo import PyMongo
import datetime

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'stealth'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/stealth'

mongo = PyMongo(app)

def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = (ord(clear[i]) + ord(key_c)) % 256
        enc.append(enc_c)
    return base64.urlsafe_b64encode(bytes(enc))

def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + enc[i] - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

def send_push_notification(title, message):
    json_data = {
    "data": {
        'title': title,
        'message': message
    },
    "to": "/topics/all"
    }

    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'key=AAAAeb9tmNo:APA91bHt7AcepAH8Q_fKzJ3vXe4l_ASGELsCA4_rgwaxPj-jhEGYSerBHlWlbwWK3jDYRbQQs2T30_0IK9-IfdnVhNC6TCs11-kG9s7qu4JtIscx7dmE1mGPYuQW4HwhFPfBWSFhCLVST1xNBwRRBjVAX00brxBhSw'
    }

    r = requests.post('https://fcm.googleapis.com/fcm/send',
        headers = headers,
        data = json.dumps(json_data))
    print(r)


@app.route('/reset_store', methods=['GET'])
def reset_store():
    store = mongo.db.store
    store.remove({})
    return 'ok'

@app.route('/reset_incoming', methods=['GET'])
def reset_incoming():
    incoming = mongo.db.incoming
    incoming.remove({})
    return 'ok'


@app.route('/add_store_messages', methods=['POST'])
def add_store():
    store = mongo.db.store
    json_form = json.loads(request.json)
    key = str(json_form['key'])
    message_in = str(json_form['message'])
    message = "%s - %s" % (message_in, datetime.datetime.now().strftime("%I:%M %p"))
    encrypt = encode(key, message)
    store.insert({'message' : encrypt})
    send_push_notification("New log", "New item added in log!")
    return 'ok'

@app.route('/get_log', methods=['POST'])
def get_messages():
    store = mongo.db.store
    json_form = json.loads(request.json)
    key = str(json.loads(json_form['key']))
    get_messages = store.find()
    messages = []
    if get_messages.count() > 0:
        for m in get_messages:
            encoded_msg = m['message']
            decoded_msg = decode(key, encoded_msg)
            messages.append(decoded_msg)

    if len(messages) > 0:
        return json.dumps({'log' : messages, 'latest' : messages[-1]})
    else:
        return json.dumps({'notification' : 'Everything seems to be wiped'})
        
@app.route('/send', methods=['POST', 'GET'])
def send():
    incoming = mongo.db.incoming
    json_form = json.loads(request.json)
    title = str(json_form['title'])
    message = str(json_form['message'])
    send_push_notification(title, message)
    con_str = "Title : %s \n Message : %s" % (title, message)
    incoming.insert({'text' : con_str})
    return 'ok'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2409)