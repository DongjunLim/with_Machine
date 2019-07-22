from flask import Flask
from flask import request
from flaskapp.get_info.store import Store
#from flaskapp.get_info,combine as cb
from flaskapp import send_data as sd


app = Flask(__name__)

@app.route("/")
def helloworld():
    return "Hello World!"
#methods=['POST']

@app.route("/data",methods=['POST'])
def receive():
    #req_json =  {request.form['store_name'],request.form['gps_lat'],request.form['gps_lon']}
    #req_json = request.get_json()
    req_json = request.json
    print(req_json)
    
    #print(req_json)
    #store_info = cb.combine_info(request.form['store_name'],request.form['gps_location'])
    #datas = sd.convert_json(store_info)

    #store = Store("starbucks","시흥시 대야동","ICON","4.5","맛있어요","cafe")
    #datas = sd.convert_json(store)
   # body = req_json.json()
    
    return req_json

