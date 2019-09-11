import sys
import os
sys.path.insert(0, './app/src/get_info')

from flask import Flask
from flask import request
from flask_autoindex import AutoIndex

from get_google import Google
from get_naver import Naver
from get_csv import csv_data
from combine import combine
from .src.db.database import DB
from .src.cdata import Cdata


app = Flask(__name__)
AutoIndex(app, browse_root='/home/ubuntu/client/')

__google = None
__naver = Naver()
__mysql_user = ""
__mysql_password = ""
__store_info = None
__data = None

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
with open("../key/db_user.txt",mode='r') as f:
    __mysql_user = f.read()
with open("../key/db_password.txt", mode='r') as f:
    __mysql_password = f.read()


@app.route("/")
def helloworld():
    return "Hello World!"

@app.route("/data",methods=['POST'])
def receive():


    global __google,__naver,__place_id,__store_info,__data

    #db = DB(__mysql_user,__mysql_password)

    req_json = request.json

    print(req_json)
    
    __data = Cdata(req_json['store_name'],req_json['gps_lat'],req_json['gps_lon'],req_json['user_language'],req_json['visit_language'])
    
    google_info = __google.get_place_info(__data)
    
    csv_info = csv_data(__data.get_name()).toJSON()
    
    naver_info = __naver.get_naver_info(__data)
    
    __store_info = combine(google_info,csv_info,naver_info)

    

    #db.set_store_query(store_info)
    #db.insert_db()
    
    return __store_info

@app.teardown_appcontext
def tesrdown_appcontext(exception):
    global __mysql_user,__mysql_password,__store_info,__data

    directory = '../client/picture/'+__store_info['place_id']
    db = DB(__mysql_user,__mysql_password,__data.get_user_language())
    db.insert_store_table(__store_info)
    db.insert_reviews_table(__store_info)
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            __google.save_photo(directory)
            db.insert_types_table(__store_info)
            print("End")
    except OSError:
        print('Error: Creating directory. ' + directory)
    db.close_db()
