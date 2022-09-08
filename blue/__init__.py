from flask import Flask
from flask_cors import CORS, cross_origin
from flask_restful import Api,Resource
from blue.api.routes import mod

app = Flask(__name__)
CORS(app)

app.register_blueprint(mod,url_prefix = '/api')
