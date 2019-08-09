import sys
sys.path.insert(0, '~/webapp/flaskapp/get_info')
from flask import Flask
from flask import request
from .get_info import receive_API as ra

app = Flask(__name__)

__API_KEY = None
with open("../api_key.txt",mode='r') as f:
    __API_KEY = f.read()

@app.route("/")
def helloworld():
    return "Hello World!"


#클라이언트와 통신하는 부분
@app.route("/data",methods=['POST'])
def receive():

    global __API_KEY

    #클라이언트로 받은 데이터를 req_json에 json 형식으로 저장
    req_json = request.json
    print(req_json)

    #저장한 데이터를 토대로 google place api에서 매장정보를 받아와
    #place_info에 저장
    place_info = ra.get_place_info(req_json['store_name'],
            req_json['gps_lat'],
            req_json['gps_lon'],
            __API_KEY)

    #받아온 정보 클라이언트에 전송
    return place_info
