import googlemaps

#좌표주소를 일반주소로 변환
def get_address(api_key,lat,lng):
    gmaps = googlemaps.Client(key=api_key)
    address = gmaps.reverse_geocode((lat,lng),language="ko")
    formatted_address = address[0].get("formatted_address")
    return formatted_address


#일반주소와 이름을 합쳐 검색키워드로 변환
def get_keyword(name,lat,lng,api_key):
    address = get_address(api_key,lat,lng)
    return address + " 주변 " + name
