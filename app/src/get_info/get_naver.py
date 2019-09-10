import os
import sys
import urllib.request
import json
from app.src.translation import translate as t

class Naver(object):
    
    def set_id(self,naver_id):
        self.__id = naver_id.rstrip('\n')
    def set_key(self,naver_key):
        self.__key = naver_key.rstrip('\n')
    def set_geo_id(self,geo_id):
        self.__geo_id = geo_id.rstrip('\n')
    def set_geo_key(self,geo_key):
        self.__geo_key = geo_key.rstrip('\n')


    def get_url_info(self,keyword):
        text = urllib.parse.quote(keyword)
        url = "https://openapi.naver.com/v1/search/local.json?query="+text
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",self.__id)
        request.add_header("X-Naver-Client-Secret",self.__key)
        return request

    def get_address_url(self,lat,lon):
	    url = "https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc?"
	    url+= "coords={:},{:}&sourcecrs=epsg:4326&orders=admcode,addr&output=json".format(lon,lat)
	    request = urllib.request.Request(url)
	    request.add_header("X-NCP-APIGW-API-KEY-ID",self.__geo_id)
	    request.add_header("X-NCP-APIGW-API-KEY",self.__geo_key)
	    return request

    def get_address(self,url):
        addr = ""
        response = urllib.request.urlopen(url)
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            contents = json.loads(response_body.decode('utf-8'))
            if (contents['status']['name']== 'no results'):
                return 0
            del contents['results'][1]['region']['area0']
            for x in contents['results'][1]['region']:
                addr += contents['results'][1]['region'][x]['name'] + " "
            return addr
        else:
            return "ERROR" + rescode

    def get_detail_naver(self,url):
        response = urllib.request.urlopen(url)
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            contents = json.loads(response_body.decode('utf-8'))
        if contents['items'] is not None:
            return contents['items'][0]['category']
        else:
            return None

    def get_naver_info(self,cdata):

        gps = cdata.get_gps()
        addr_url = self.get_address_url(gps['gps_lat'],gps['gps_lon'])
        keyword = self.get_address(addr_url)
        if(keyword==0):
    	    return None
        keyword += cdata.get_name()
        search_url = self.get_url_info(keyword)
        info = self.get_detail_naver(search_url)
        info = t.translate_language(info,cdata.get_user_language())
        return info
