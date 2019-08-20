#from flaskapp import convert_keyword as ck
import requests
from flaskapp.get_info import csv_data as csv
import json


def search_url(key, name):
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"
    url += "key={:}&input={:s}&inputtype=textquery".format(key,name)
    url += "&fields=place_id"
    return url

def nearbysearch_url(key,lat,lon,name):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    url += "key={:s}&location={},{}&radius=150&language=ko&keyword={:s}".format(key,lat,lon,name)
    return url


def detail_url(key, place_id,language):
    url = "https://maps.googleapis.com/maps/api/place/details/json?"
    url += "key={:s}&language={:s}&placeid={:s}".format(key,language,place_id)
    url += "&fields=name,address_components,formatted_address,rating,review,price_level,user_ratings_total,international_phone_number,photo,type"
    return url

def photo_url(key, photo_ref):
    url = "https://maps.googleapis.com/maps/api/place/photo?"
    url+= "key={:s}&photoreference={:s}".format(key,photo_ref)
    url+= "&maxwidth=100&maxheight=100"
    return url


def get_place_id(key,name):

    response = requests.get(url=search_url(key,name))

    place_info = response.json()

    if not place_info['candidates']:
        return False

    if place_info['status']!='OK':
        return False

    candidate = place_info['candidates'][0]
    return candidate['place_id']

def get_detail(api_key,place_id,name,language):
    response = requests.get(url=detail_url(api_key,place_id,language))
    detail_info = response.json()
   
    csv_info = csv.csv_data(name).toJSON()
    detail_info.update(csv_info)
    #info = {key: value for (key, value) in (detail_info.items() + csv_info.items())}
    return detail_info


def get_photos(api_key,photos):
    
    #for x in photos:
    response = requests.get(url=photo_url(api_key,photos))
    #responses = response.json()
    print(response.content)
    return 0




def get_place_info(keyword,key,name,language):


    place_id = get_place_id(key,keyword)
    

    if place_id is False:
        return {"store_name":"Not Found",
                "gps_lat": 0,
                "gps_lon":0}

    detail = get_detail(key,place_id,name,language)
    return detail

