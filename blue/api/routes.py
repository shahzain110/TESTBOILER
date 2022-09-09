import os
import sys
from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
### change the "/" to "\\" if you are windows user ###


dirname = os.path.dirname(os.path.abspath(__file__))
dirname_list = dirname.split("/")[:-1]
dirname = "/".join(dirname_list)
print(dirname)
path = dirname + "/api"
print(path)
sys.path.append(path)

mod = Blueprint('api', __name__)
api = Api(mod)


###importing the functions from other files ###
# print(f"HEY {os.getcwd()}")
from functions import pose_detection

class intro_to_API(Resource):
    def post(self):
        try:
            import os
            cwd = os.getcwd()
            print(f"path is: {cwd}")
            video_01_path = 'videos/1.mp4'
            video_02_path = 'videos/2.mp4'
            sources = []
            video_01 = request.files['vid1'].read()
            sources.append(video_01_path)
            f = open(video_01_path, 'wb')
            f.write(video_01)
            f.close()
            video_02 = request.files['vid2'].read()
            f = open(video_02_path, 'wb')
            sources.append(video_02_path)
            f.write(video_02)
            f.close()
            match_perc = pose_detection(sources)
            dic = {"status": 200, "msg": match_perc}
        except Exception as e:
            print(e)
            dic = {"status": 444, "msg": "faliure"}
        return jsonify(dic)


api.add_resource(intro_to_API, "/intro_to_API")