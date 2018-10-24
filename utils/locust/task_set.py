from locust import HttpLocust, TaskSet, task
import random
import uuid
import json

MIN_WAIT_TIME = 5000
MAX_WAIT_TIME = 15000
PATH = '/api/v1.0{0}'
API_KEY = 'api-key'
METHODS = ['delete', 'get', 'post', 'put']


class UserAction(TaskSet):

    def on_start(self):
        self.sender = "message-sender"
        self.payloads = [
            # good payload
            # httpbin
            {
                "messageId": str(uuid.uuid4()),
                "senderId": self.sender,
                "recipients": [
                    "0700000000", "0700000001", "0700000002", "0700000003"
                ],
                "messageType": "dummy",
                "channel": "httpbin",
                "message": "This is an example message",
                "priority": "normal",
                "callback": "https://mydomain.com/callback/y7sdxl24df"
            },
            # africas-talking
            {
                "messageId": str(uuid.uuid4()),
                "senderId": "0722000000",
                "recipients": [
                    "0700000000", "0700000001", "0700000002", "0700000003"
                ],
                "messageType": "sms",
                "channel": "africas-talking",
                "message": "This is an example message",
                "priority": "normal",
                "callback": "https://mydomain.com/callback/y7sdxl24df"
            },
            # firebase
            {
                "messageId": str(uuid.uuid4()),
                "senderId": self.sender,
                "recipients": [
                    "0700000000", "0700000001", "0700000002", "0700000003"
                ],
                "messageType": "push",
                "channel": "firebase",
                "message": "This is an example message",
                "priority": "normal",
                "callback": "https://mydomain.com/callback/y7sdxl24df"
            },
            # smpp
            {
                "messageId": str(uuid.uuid4()),
                "senderId": self.sender,
                "recipients": [
                    "0700000000", "0700000001", "0700000002", "0700000003"
                ],
                "messageType": "sms",
                "channel": "smpp",
                "message": "This is an example message",
                "priority": "normal",
                "callback": "https://mydomain.com/callback/y7sdxl24df"
            },
            # bad payload
            {
                "messageId": str(uuid.uuid4())
            },
        ]

        self.headers = [
            # correct auth headers
            {
                'Content-type': 'application/json',
                'Authorization': API_KEY
            },
            # wrong api-key
            {
                'Content-type': 'application/json',
                'Authorization': 'wrong'
            }
        ]

    @task(2)
    def send_message(self):
        for method in METHODS:
            payload = self.payloads[random.randint(0, 3)]
            payload["messageId"] = str(uuid.uuid4())
            getattr(self.client, method)(
                PATH.format('/sendMessage'),
                data=json.dumps(payload),
                headers=self.headers[random.randint(0, 1)]
            )

            # make a good request
            payload = self.payloads[random.randint(0, 3)]
            payload["messageId"] = str(uuid.uuid4())
            self.client.post(
                PATH.format('/sendMessage'),
                data=json.dumps(payload),
                headers=self.headers[0]
            )

    @task(1)
    def check_health(self):
        for method in METHODS:
            getattr(self.client, method)(
                PATH.format('/checkHealth'),
                data=json.dumps(self.payloads[random.randint(0, 3)]),
                headers=self.headers[random.randint(0, 1)]
            )
            # make a good request
            self.client.get(
                PATH.format('/checkHealth'),
                headers=self.headers[0]
            )


class User(HttpLocust):
    task_set = UserAction
    min_wait = MIN_WAIT_TIME
    max_wait = MAX_WAIT_TIME
