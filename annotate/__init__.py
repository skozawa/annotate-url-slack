from flask import Flask

from flask_restful import Api

from annotate.config import config


app = Flask(__name__)
app.config.from_object(config)

api = Api(app)

import annotate.web
