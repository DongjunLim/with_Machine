import googlemaps

def get_address(api_key,lat,lng):
    gmaps = googlemaps.Client(key=api_key)
    address = gmaps.reverse_geocode((lat,lng),language="ko")
    formatted_address = address[0].get("formatted_address")
    return formatted_address


def get_keyword(name,lat,lng,api_key):
    address = get_address(api_key,lat,lng)
    return address + " 주변 " + name
