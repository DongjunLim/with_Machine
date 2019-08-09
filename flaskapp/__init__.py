import sys
sys.path.insert(0, '~/webapp/flaskapp/get_info')
from flask import Flask
from flask import request
from .get_info import receive_API as ra
from .get_info import get_naver as naver
from flaskapp import convert_keyword as ck

app = Flask(__name__)

__GOOGLE_KEY = None
__NAVER_ID = None
__NAVER_KEY = None

with open("../api_key.txt",mode='r') as f:
    __GOOGLE_KEY = f.read()

#with open("../naver_id.txt",mode='r') as f:
#    __NAVER_ID = f.read()

#with open("../naver_key.txt",mode='r') as f:
#    __NAVER_KEY = f.read()

__NAVER_ID = "yg2J11VD2cyLS60KO81e"
__NAVER_KEY = "l8cpvfrzQ4"



@app.route("/")
def helloworld():
    return "Hello World!"


#?¥Îùº?¥Ïñ∏?∏Ï? ?µÏã†?òÎäî Î∂ÄÎ∂?
@app.route("/data",methods=['POST'])
def receive():

    global __GOOGLE_KEY,__NAVER_ID,__NAVER_KEY

    #?¥Îùº?¥Ïñ∏?∏Î°ú Î∞õÏ? ?∞Ïù¥?∞Î? req_json??json ?ïÏãù?ºÎ°ú ?Ä??    
    req_json = request.json
    print(req_json)

    store_name = req_json['store_name']
    gps_lat = req_json['gps_lat']
    gps_lon = req_json['gps_lon']

    keyword = ck.get_keyword(store_name,gps_lat,gps_lon,__GOOGLE_KEY,"ko")

    #?Ä?•Ìïú ?∞Ïù¥?∞Î? ?†Î?Î°?google place api?êÏÑú Îß§Ïû•?ïÎ≥¥Î•?Î∞õÏïÑ?Ä
    #place_info???Ä??    
    store_info = ra.get_place_info(keyword,
            __GOOGLE_KEY,store_name)

    naver_info = naver.get_naver_info(keyword,
            __NAVER_ID,
            __NAVER_KEY)

    store_info['result']['types'].append(naver_info)
    #ra.get_photos(__GOOGLE_KEY,store_info['result']['photos'][0]['photo_reference'])
    #print(store_info['result']['photos'][0]['photo_reference'])
    #Î∞õÏïÑ???ïÎ≥¥ ?¥Îùº?¥Ïñ∏?∏Ïóê ?ÑÏÜ°
    return store_info
