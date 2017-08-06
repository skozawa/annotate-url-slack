import json

from flask_restful import Resource
from flask_restful import reqparse

from annotate.spread import Gspread
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
        if callback_id == 'quality_metrics':
            return slack_req.QualityMetricsRequest(payload)
        if callback_id == 'evaluate_metric':
            req = slack_req.EvaluateMetricRequest(payload)
            gspread = Gspread()
            gspread.update_url_score(req.resource_url(), req.user_name, req.attr, req.value)
            return req
        return slack_req.ActionRequest(payload)
