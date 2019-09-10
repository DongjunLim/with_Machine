import urllib.request
import os
import json
import googlemaps
import requests
from app.src.translation import translate as t
from app.src import store

class Google(object):
    __store_info = None
    __place_id = ""
    __photo_ref = None

    def __init__(self,api_key):
        self.__key = api_key


    def get_address(self,gps_lat,gps_lon,country):
        gmaps = googlemaps.Client(key=self.__key)
        address = gmaps.reverse_geocode((gps_lat,gps_lon),language=country)
        formatted_address = address[0].get("formatted_address")
        print(formatted_address)
        return formatted_address

    def set_keyword(self,cdata):
        name = cdata.get_name()
        gps = cdata.get_gps()
        language = cdata.get_visit_language()
        address = self.get_address(gps['gps_lat'],gps['gps_lon'],language)
        self.__keyword = name + " nearby " + address
       
    def set_search_url(self,cdata):
        gps = cdata.get_gps()

        url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"
        url += "key={:}&input={:s}&inputtype=textquery".format(self.__key,self.__keyword)
        url += "&fields=place_id"
        url += "&language={:s}".format(cdata.get_visit_language())
        url += "&locationbias=circle:200:{:},{:}".format(gps['gps_lat'],gps['gps_lon'])
        return url

    '''
    def nearbysearch_url(self,key,lat,lon,name):
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        url += "key={:s}&location={},{}&radius=150&language=ko&keyword={:s}".format(key,lat,lon,name)
        return url
    '''

    def set_detail_url(self,place_id,user_language):
        url = "https://maps.googleapis.com/maps/api/place/details/json?"
        url += "key={:s}&language={:s}&placeid={:s}".format(self.__key,user_language,place_id)
        url += "&fields=place_id,name,address_components,formatted_address,rating,review,price_level,international_phone_number,photo,type"
        return url

    
    def photo_url(self,photo_ref):
        url = "https://maps.googleapis.com/maps/api/place/photo?"
        url+= "key={:s}&photoreference={:s}".format(self.__key,photo_ref)
        url+= "&maxwidth=300&maxheight=200"
        return url
    

    def get_place_id(self,cdata):

        response = requests.get(url=self.set_search_url(cdata))

        place_info = response.json()

        if not place_info['candidates']:
            return False

        if place_info['status']!='OK':
            return False

        candidate = place_info['candidates'][0]
        self.__place_id = candidate['place_id']
        return self.__place_id

    def get_detail(self,cdata,place_id):
        response = requests.get(url=self.set_detail_url(place_id,cdata.get_user_language()))

        detail = response.json()

        self.__store_info = store.Store(detail['result'])
        
        #self.__photo = detail['result']

    
    def get_photos(self,photos):
        response = requests.get(url=photo_url(photos))
        return response.url

    def save_photo(self):
        directory = '/home/ubuntu/client/picture/'+self.__place_id
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
                for idx,photo in enumerate(self.__photo_ref):
                    response = requests.get(url=self.photo_url(photo['photo_reference']))
                    file_name = directory + "/{:s}.jpg".format(str(idx))
                    urllib.request.urlretrieve(response.url,file_name)
                    if idx >= 4:
                        break
        except OSError:
            print('Error: Creating directory. ' + directory)

    def get_place_info(self,cdata):

        self.set_keyword(cdata)

        place_id = self.get_place_id(cdata)
    
        if place_id is False:
            print("FOUND ERROR")
            return {"store_name":"Not Found",
                    "gps_lat": 0,
                    "gps_lon":0}

        self.get_detail(cdata,place_id)

        result = self.__store_info.get_info()
        self.__photo_ref = self.__store_info.get_photo()



               

        for x in result['reviews']:
            x['text'] = t.translate_language(x['text'],cdata.get_user_language())
        for y in result['types']:
            y = t.translate_language(y,cdata.get_user_language())
        return result
