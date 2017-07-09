from flask_restful import Resource

from annotate import api
from annotate import app


class Root(Resource):
    """dispatch /."""
    def get(self):
        return {'message': 'Hello'}


class SlackAction(Resource):
    def post(self):
        return {}


class SlackOptions(Resource):
    def post(self):
        return {}


api.add_resource(Root, '/')
api.add_resource(SlackAction, '/slack/action')
api.add_resource(SlackOption, '/slack/options')
