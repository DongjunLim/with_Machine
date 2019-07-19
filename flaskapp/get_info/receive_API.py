import requests

__API_KEY = None


def load_api_key(path):
    with open(path, mode='r') as f:
        global __API_KEY
        __API_KEY = f.read()


def search_url(key, name):
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"
    url += "key = {:s}&input={:s}&inputtype=textquery".format(key,name)
    url += "&fields=place_id"
    return url

def detail_url(key, place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json?"
    url += "key = {:s}&place_id{:s}".format(key,place_id)
    url += "&fields=name,formatted_address,icon,review,price_level,user_ratings_total,international_phone_number,photo,type"
    return url



