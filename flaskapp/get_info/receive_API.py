from flaskapp import convert_keyword as ck
import requests
from flaskapp.get_info import csv_data as csv



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

def photo_url(key, photo_ref):
    url = "https://maps.googleapis.com/maps/api/place/photo?"
    url+= "key={:s}&photoreference={:s}".format(key,photo_ref)
    url+= "&maxwidth=100&maxheight=100"
    return url


#ë§¤ì¥ id ë¥??»ì–´?¤ëŠ” ?¨ìˆ˜
def get_place_id(api_key, keyword):

    response = requests.get(url=search_url(api_key,keyword))

    place_info = response.json()

    if not place_info['candidates']:
        return False

    if place_info['status']!='OK':
        return False

    candidate = place_info['candidates'][0]
    return candidate['place_id']

#?ì„¸ë§¤ì¥?•ë³´ë¥??»ì–´?¤ëŠ” ?¨ìˆ˜
def get_detail(api_key,place_id,name):
    response = requests.get(url=detail_url(api_key,place_id))
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




#ë§¤ì¥?´ë¦„ê³??„ì¹˜?•ë³´ë¥?ë°›ì•„ ?ì„¸ë§¤ì¥?•ë³´ë¥?ë°˜í™˜?˜ëŠ” ?¨ìˆ˜
def get_place_info(keyword,api_key,name):


    #ê²€?‰í‚¤?Œë“œë¡?google places api???‘ê·¼??    #?¸ë?ê²€?‰ì„ ?„í•œ ë§¤ì¥ idë¥?ë°›ì•„??
    place_id = get_place_id(api_key,keyword)
    print(keyword)

    #ë°›ì•„???•ë³´ê°€ ?†ì„ê²½ìš°
    if(place_id == False):
        return {"store_name":"Not Found",
                "gps_lat": 0,
                "gps_lon":0}

    #ë§¤ì¥ idë¥??µí•´ ?¸ë??•ë³´ë¥??»ì–´????ë°˜í™˜
    detail = get_detail(api_key,place_id,name)
    return detail

