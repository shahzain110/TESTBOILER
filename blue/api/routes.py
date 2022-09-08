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
            sources = []
            video_01 = request.files['vid1'].read()
            # print("Type: ------------------->", type(video_01))
            video_01_path = '/home/shahzain/Documents/GitHub/PoseEst_dep/PoseEst/resouces/1.mp4'
            sources.append(video_01_path)
            f = open(video_01_path, 'wb')
            f.write(video_01)
            f.close()

            video_02 = request.files['vid2'].read()
            # print("Type: ------------------->", type(video_02))
            video_02_path = '/home/shahzain/Documents/GitHub/PoseEst_dep/PoseEst/resouces/2.mp4'
            f = open(video_02_path, 'wb')
            sources.append(video_02_path)
            f.write(video_02)
            f.close()
            match_perc = detection(sources)
            dic = {"status": 200, "msg": match_perc}
            return jsonify(dic)
        except Exception as e:
            dic = {"status":444,"msg":"faliure"}
            return jsonify(dic)


api.add_resource(intro_to_API, "/intro_to_API")
