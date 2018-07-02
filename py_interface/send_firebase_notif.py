import json
import requests

title = str(input("Enter your title : "))
message = str(input("Enter your message : "))
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