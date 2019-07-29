from flaskapp.get_info import convert_keyword as ck
import requests

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
    url += "key={:s}&placeid={:s}".format(key,place_id)
    url += "&fields=name,formatted_address,icon,review,price_level,user_ratings_total,international_phone_number,photo,type"
    return url

def get_place_id(api_key, keyword):

    response = requests.get(url=search_url(api_key,keyword))

    place_info = response.json()

    if not place_info['candidates']:
        return False

    if place_info['status']!='OK':
        return False

    candidate = place_info['candidates'][0]
    return candidate['place_id']

def get_detail(api_key,place_id):
    response = requests.get(url=detail_url(api_key,place_id))
    detail_info = response.json()
    return detail_info

def get_place_info(name,lat,lng,api_key):
    keyword = ck.get_keyword(name,lat,lng,api_key)
    place_id = get_place_id(api_key,keyword)

    if(place_id == False):
        return {"store_name":"Not Found",
                "gps_lat": 0,
                "gps_lon":0}

    detail = get_detail(api_key,place_id)
    return detail
