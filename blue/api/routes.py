from flask import Blueprint,jsonify, request
from flask_restful import Api,Resource
from werkzeug.utils import secure_filename


import sys 
import os
import json

### change the "/" to "\\" if you are windows user ###


dirname = os.path.dirname(os.path.abspath(__file__))
dirname_list = dirname.split("/")[:-1]
dirname = "/".join(dirname_list)
print(dirname)
path = dirname + "/api"
print(path)
sys.path.append(path)


mod = Blueprint('api',__name__)
api = Api(mod)

###importing the functions from other files ###

from functions import basic_function


class intro_to_API(Resource):
    def get(self):
        try:
            basic_function()
            dic = {"status":200,"msg":"ok"}
            return jsonify(dic)
        except Exception as e:
            dic = {"status":444,"msg":"faliure"}
            return jsonify(dic)


api.add_resource(intro_to_API, "/intro_to_API")
