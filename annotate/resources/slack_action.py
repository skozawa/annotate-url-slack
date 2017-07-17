import json

from flask_restful import Resource
from flask_restful import reqparse

import annotate.slack.request as slack_req

class SlackAction(Resource):
    def post(self):
        payload = self.get_payload()
        print(payload)
        req = self.payload_to_request(payload)
        if not req:
            return {}
        return req.response()

    def get_payload(self):
        parser = reqparse.RequestParser()
        parser.add_argument('payload', required=True, type=json.loads)
        args = parser.parse_args()
        return args['payload']

    def payload_to_request(self, payload):
        callback_id = payload.get('callback_id', None)
        if callback_id is None:
            return None
        if callback_id == 'annotate_url_request':
            return slack_req.AnnotateUrlRequest(payload)
        return slack_req.ActionRequest(payload)
