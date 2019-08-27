import googlemaps
from flaskapp.cdata import Cdata

#좌표주소를 일반주소로 변환
def get_address(api_key,lat,lng,country):
    gmaps = googlemaps.Client(key=api_key)
    address = gmaps.reverse_geocode((lat,lng),language=country)
    formatted_address = address[0].get("formatted_address")
    return formatted_address


#일반주소와 이름을 합쳐 검색키워드로 변환
def get_keyword(Cdata,api_key):
    
    name = Cdata.get_name()
    gps = Cdata.get_gps()
    language = Cdata.get_visit_language()
    address = get_address(api_key,gps['gps_lat'],gps['gps_lon'],language)

    return name + " nearby " + address
