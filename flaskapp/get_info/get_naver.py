import os
import sys
import urllib.request
import json
from flaskapp.translation import translate as t


def set_url_info(keyword,naver_id, naver_key):
    text = urllib.parse.quote(keyword)
    url = "https://openapi.naver.com/v1/search/local.json?query="+text
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",naver_id)
    request.add_header("X-Naver-Client-Secret",naver_key)
    return request

def set_address_url(lat,lon,naver_id,naver_key):
	url = "https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc?"
	url+= "coords={:},{:}&sourcecrs=epsg:4326&orders=admcode,addr&output=json".format(lon,lat)
	request = urllib.request.Request(url)
	request.add_header("X-NCP-APIGW-API-KEY-ID",naver_id)
	request.add_header("X-NCP-APIGW-API-KEY",naver_key)
	return request

def get_address(url):
	response = urllib.request.urlopen(url)
	rescode = response.getcode()
	if(rescode==200):
		response_body = response.read()
		contents = json.loads(response_body.decode('utf-8'))
		if(contents['status']['name']=='no results'):
			return 0
		addr =  contents['results'][0]['region']['area1']['name'] + " "
		addr += contents['results'][0]['region']['area2']['name'] + " "
		addr += contents['results'][0]['region']['area3']['name'] + " "
		

		return addr
	else:
		return "ERROR" + rescode



def get_detail_naver(url):
    response = urllib.request.urlopen(url)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        contents = json.loads(response_body.decode('utf-8'))
        print(contents)
    if contents['items'] is not None:
        return contents['items'][0]['category']
    else:
        return None
        

def get_naver_info(store_name,gps_lat,gps_lon,n_id,n_key,geo_id,geo_key,language):
    addr_url = set_address_url(gps_lat,gps_lon,geo_id,geo_key)
    keyword = get_address(addr_url)
    if(keyword==0):
    	return None
    keyword += store_name
    search_url = set_url_info(keyword,n_id,n_key)
    info = get_detail_naver(search_url)
    info = t.translate_language(info,language)
    return info
