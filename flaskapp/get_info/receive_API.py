from flaskapp.get_info import convert_keyword as ck
import requests
from flaskapp.get_info import csv_data as csv

__API_KEY = None

def load_api_key(path):
    with open(path, mode='r') as f:
        global __API_KEY
        __API_KEY = f.read()


def search_url(key, name):
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"
    url += "key={:s}&input={:s}&inputtype=textquery".format(key,name)
    url += "&fields=place_id"
    return url

def detail_url(key, place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json?"
    url += "key={:s}&language=en&placeid={:s}".format(key,place_id)
    url += "&fields=name,formatted_address,icon,rating,review,price_level,user_ratings_total,international_phone_number,photo,type"
    return url


#매장 id 를 얻어오는 함수
def get_place_id(api_key, keyword):

    response = requests.get(url=search_url(api_key,keyword))

    place_info = response.json()

    if not place_info['candidates']:
        return False

    if place_info['status']!='OK':
        return False

    candidate = place_info['candidates'][0]
    return candidate['place_id']

#상세매장정보를 얻어오는 함수
def get_detail(api_key,place_id):
    response = requests.get(url=detail_url(api_key,place_id))
    detail_info = response.json()
    #csv_info = csv.csv_data().toJSON()
    #info = {key: value for (key, value) in (detail_info.items() + csv_info.items())}
    return detail_info


#매장이름과 위치정보를 받아 상세매장정보를 반환하는 함수
def get_place_info(name,lat,lng,api_key):

    #매장이름과 위치정보를 검색키워드로 변환
    keyword = ck.get_keyword(name,lat,lng,api_key)

    #검색키워드로 google places api에 접근해
    #세부검색을 위한 매장 id를 받아옴 
    place_id = get_place_id(api_key,keyword)
    print(keyword)

    #받아온 정보가 없을경우
    if(place_id == False):
        return {"store_name":"Not Found",
                "gps_lat": 0,
                "gps_lon":0}

    #매장 id를 통해 세부정보를 얻어온 후 반환
    detail = get_detail(api_key,place_id)
    return detail
