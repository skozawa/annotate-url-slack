from flask_restful import Resource

from annotate import api
from annotate import app

class Root(Resource):
    """dispatch /."""
    def get(self):
        return {'message': 'Hello'}


api.add_resource(Root, '/')
