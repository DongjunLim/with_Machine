import os
import sys
import urllib.request
import json



def create_url_info(keyword,naver_id, naver_key):
    text = urllib.parse.quote(keyword)
    url = "https://openapi.naver.com/v1/search/local.json?query="+text
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",naver_id)
    request.add_header("X-Naver-Client-Secret",naver_key)
    return request


def get_detail_naver(url):
    response = urllib.request.urlopen(url)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        contents = json.loads(response_body.decode('utf-8'))
        return contents['items'][0]['category']
    else:
        return "ERROR: " + rescode
        

def get_naver_info(keyword,n_id,n_key):
    url = create_url_info(keyword,n_id,n_key)
    info = get_detail_naver(url)
    print(info)
    return info

    
