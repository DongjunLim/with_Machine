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


#매장 id �??�어?�는 ?�수
def get_place_id(api_key, keyword):

    response = requests.get(url=search_url(api_key,keyword))

    place_info = response.json()

    if not place_info['candidates']:
        return False

    if place_info['status']!='OK':
        return False

    candidate = place_info['candidates'][0]
    return candidate['place_id']

#?�세매장?�보�??�어?�는 ?�수
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




#매장?�름�??�치?�보�?받아 ?�세매장?�보�?반환?�는 ?�수
def get_place_info(keyword,api_key,name):


    #검?�키?�드�?google places api???�근??    #?��?검?�을 ?�한 매장 id�?받아??
    place_id = get_place_id(api_key,keyword)
    print(keyword)

    #받아???�보가 ?�을경우
    if(place_id == False):
        return {"store_name":"Not Found",
                "gps_lat": 0,
                "gps_lon":0}

    #매장 id�??�해 ?��??�보�??�어????반환
    detail = get_detail(api_key,place_id,name)
    return detail

