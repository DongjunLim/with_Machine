from flaskapp import convert_keyword as ck
import requests
from flaskapp.get_info import csv_data as csv
from flaskapp.translation import translate as t
from flaskapp import store
import json

class Google(object):
    __store_info = None
    __place_id = None
    def __init__(self,api_key):
        self.__key = api_key
       
    def set_search_url(self,cdata,keyword):
        gps = cdata.get_gps()

        url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"
        url += "key={:}&input={:s}&inputtype=textquery".format(self.__key,keyword)
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

    '''
    def photo_url(self,key, photo_ref):
        url = "https://maps.googleapis.com/maps/api/place/photo?"
        url+= "key={:s}&photoreference={:s}".format(key,photo_ref)
        url+= "&maxwidth=100&maxheight=100"
        return url
    '''

    def get_place_id(self,cdata,keyword):

        response = requests.get(url=self.set_search_url(cdata,keyword))

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
        

        '''
        csv_info = csv.csv_data(cdata.get_name()).toJSON()
        self.__store_info.update(csv_info)

    
    def get_photos(self,api_key,photos):
    
       #for x in photos:
        response = requests.get(url=photo_url(api_key,photos))
        #responses = response.json()
        print(response.content)
        return 0
    '''
    def get_place_info(self,cdata,keyword):

        place_id = self.get_place_id(cdata,keyword)
    
        if place_id is False:
            return {"store_name":"Not Found",
                    "gps_lat": 0,
                    "gps_lon":0}

        self.get_detail(cdata,place_id)

        result = self.__store_info.get_info()

        for x in result['reviews']:
            x['text'] = t.translate_language(x['text'],cdata.get_user_language())
        for y in result['types']:
            y = t.translate_language(y,cdata.get_user_language())

        return result
