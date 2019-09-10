import sys
sys.path.insert(0, './app/src/get_info')

from flask import Flask
from flask import request
from flask_autoindex import AutoIndex

from get_google import Google
from get_naver import Naver
from get_csv import csv_data
from combine import combine

from .src.cdata import Cdata


app = Flask(__name__)
AutoIndex(app, browse_root='/home/ubuntu/client/')

__google = None
__naver = Naver()

with open("../key/google_key.txt",mode='r') as f:
    __google = Google(f.read())
with open("../key/naver_id.txt",mode='r') as f:
    __naver.set_id(f.read())
with open("../key/naver_key.txt",mode='r') as f:
    __naver.set_key(f.read())
with open("../key/naver_geo_id.txt",mode='r') as f:
	__naver.set_geo_id(f.read())
with open("../key/naver_geo_key.txt", mode='r') as f:
	__naver.set_geo_key(f.read())



@app.route("/")
def helloworld():
    return "Hello World!"

@app.route("/data",methods=['POST'])
def receive():

    global __google,__naver

    req_json = request.json

    print(req_json)
    
    data = Cdata(req_json['store_name'],req_json['gps_lat'],req_json['gps_lon'],req_json['user_language'],req_json['visit_language'])
    
    google_info = __google.get_place_info(data)
    
    csv_info = csv_data(data.get_name()).toJSON()
    
    naver_info = __naver.get_naver_info(data)
    
    store_info = combine(google_info,csv_info,naver_info)
    
    return store_info

@app.teardown_appcontext
def tesrdown_appcontext(exception):
    #print("준???)
    __google.save_photo()
    #print("??료")
