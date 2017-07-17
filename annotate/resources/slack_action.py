import json

from flask_restful import Resource
from flask_restful import reqparse

import annotate.slack.request as slack_req

class SlackAction(Resource):
    def post(self):
        payload = self.get_payload()
        print(payload)
        req = self.payload_to_request(payload)
        if req and req.action_is_ok:
            return {'text': 'yes'}
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
