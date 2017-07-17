from flask_restful import Resource

from annotate import api
from annotate import app

from annotate.resources.slack_action import SlackAction


class Root(Resource):
    """dispatch /."""
    def get(self):
        return {'message': 'Hello'}


class SlackOptions(Resource):
    def post(self):
        return {}


api.add_resource(Root, '/')
api.add_resource(SlackAction, '/slack/action')
api.add_resource(SlackOptions, '/slack/options')
