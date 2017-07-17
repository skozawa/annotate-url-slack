import json

from flask_restful import Resource

from flask_restful import reqparse

class SlackAction(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('payload', required=True, type=json.loads)
        args = parser.parse_args()
        print(args)
        return {}

    
