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
#methods=['POST']

@app.route("/data",methods=['POST'])
def receive():
    global __API_KEY
    req_json = request.json
    print(req_json)
    place_info = ra.get_place_info(req_json['store_name'],
            req_json['gps_lat'],
            req_json['gps_lon'],
            __API_KEY)
    return place_info



    
    

