import sys
sys.path.insert(0, '~/webapp/flaskapp/get_info')
from flask import Flask
from flask import request
from .get_info import get_google as gg
from .get_info import get_naver as naver
from flaskapp import convert_keyword as ck

app = Flask(__name__)

__GOOGLE_KEY = None
__NAVER_ID = None
__NAVER_KEY = None
__NAVER_GEO_ID = None
__NAVER_GEO_KEY = None


with open("../api_key.txt",mode='r') as f:
    __GOOGLE_KEY = f.read()

with open("../naver_id.txt",mode='r') as f:
    __NAVER_ID = f.read()
    __NAVER_ID = __NAVER_ID.rstrip('\n')

with open("../naver_key.txt",mode='r') as f:
    __NAVER_KEY = f.read()
    __NAVER_KEY = __NAVER_KEY.rstrip('\n')

with open("../naver_geo_id.txt",mode='r') as f:
	__NAVER_GEO_ID = f.read()
	__NAVER_GEO_ID = __NAVER_GEO_ID.rstrip('\n')
with open("../naver_geo_key.txt", mode='r') as f:
	__NAVER_GEO_KEY = f.read()
	__NAVER_GEO_KEY = __NAVER_GEO_KEY.rstrip('\n')

@app.route("/")
def helloworld():
    return "Hello World!"

@app.route("/data",methods=['POST'])
def receive():

    global __GOOGLE_KEY,__NAVER_ID,__NAVER_KEY,__NAVER_GEO_ID,__NAVER_GEO_KEY

    req_json = request.json

    store_name = req_json['store_name']
    gps_lat = req_json['gps_lat']
    gps_lon = req_json['gps_lon']
    user_language = req_json['user_language']
    visit_language = req_json['visit_language']

    
    keyword = ck.get_keyword(store_name,gps_lat,gps_lon,__GOOGLE_KEY,visit_language)
    
    store_info = gg.get_place_info(keyword,
            __GOOGLE_KEY,store_name,user_language,gps_lat,gps_lon,visit_language)

    naver_info = naver.get_naver_info(store_name,gps_lat,gps_lon,__NAVER_ID,__NAVER_KEY,__NAVER_GEO_ID,__NAVER_GEO_KEY,user_language)
    if naver_info is not None:
        store_info['result']['types'].append(naver_info)

    return store_info
