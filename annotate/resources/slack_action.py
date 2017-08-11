import json

from flask_restful import Resource
from flask_restful import reqparse

from annotate.spread import Gspread

from annotate import connect_db

import annotate.service.annotation as annotation_service
import annotate.service.entry as entry_service
import annotate.slack.request as slack_req
import annotate.slack.response as slack_res

class SlackAction(Resource):
    def post(self):
        payload = self.get_payload()
        print(payload)
        callback_id = payload.get('callback_id', None)
        if callback_id is None:
            return {}
        elif callback_id == 'quality_metrics':
            return self.quality_metrics(payload)
        elif callback_id == 'evaluate_metric':
            return self.evaluate_metric(payload)
        else:
            return {}

    def get_payload(self):
        parser = reqparse.RequestParser()
        parser.add_argument('payload', required=True, type=json.loads)
        args = parser.parse_args()
        return args['payload']

    def quality_metrics(self, payload):
        req = slack_req.OptionsRequest(payload)
        res = slack_res.EvaluateResponse(req.value, req.resource_url())
        return res.response()

    def evaluate_metric(self, payload):
        req = slack_req.EvaluateMetricRequest(payload)
        db = connect_db()
        entry = entry_service.find_or_create_entry(db, req.resource_url())
        annotation = annotation_service.update_or_create(
            db, entry.id, req.user_name, req.attr, int(req.value)
        )

        scores = annotation.score()
        scores[req.attr] = int(req.value)
        res = slack_res.OptionsResponse(req.resource_url(), scores=scores)

        return res.response()
