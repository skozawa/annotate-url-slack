from flask import Flask
from flask import g

from flask_restful import Api

from annotate.config import config
from annotate.db import DB


app = Flask(__name__)
app.config.from_object(config)

api = Api(app)

def connect_db():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = DB()
    return db

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_db', None)
    if db is not None:
        db.close()

import annotate.web
