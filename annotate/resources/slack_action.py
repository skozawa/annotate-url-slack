import json

from flask_restful import Resource
from flask_restful import reqparse

import annotate.slack.request as slack_req

class SlackAction(Resource):
    def post(self):
        payload = self.get_payload()
        print(payload)
        req = self.payload_to_request(payload)
        if req and req.action_is_ok():
            return {'text': req.original_text, 'attachments': [self.attachment(target) for target in ['reading', 'funny', 'topic', 'completely']]}
        else:
            return {'text': 'no'}

    def get_payload(self):
        parser = reqparse.RequestParser()
        parser.add_argument('payload', required=True, type=json.loads)
        args = parser.parse_args()
        return args['payload']

    def payload_to_request(self, payload):
        callback_id = payload.get('callback_id', None)
        if callback_id is None:
            return None
        return slack_req.ActionRequest(payload)

    def attachment(self, target):
        return {
            "text": target,
            "callback_id": "annotation",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "score",
                    "text": "1",
                    "type": "button",
                    "value": 1,
                },
                {
                    "name": "score",
                    "text": "2",
                    "type": "button",
                    "value": 2,
                },
                {
                    "name": "score",
                    "text": "3",
                    "type": "button",
                    "value": 3,
                },
                {
                    "name": "score",
                    "text": "4",
                    "type": "button",
                    "value": 4,
                },
                {
                    "name": "score",
                    "text": "5",
                    "type": "button",
                    "value": 5,
                },
            ]
        }
