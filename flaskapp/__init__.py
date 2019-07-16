from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def helloworld():
    return "Hello World!"

@app.route("/data",methods=['POST'])
def receive():
    req_json =  {request.form['storeName'],request.form['gpsLocation']} #request.get_json()
    print(req_json)
    datas = {
            'a' : 'Hi client'
            }

    return request.url

