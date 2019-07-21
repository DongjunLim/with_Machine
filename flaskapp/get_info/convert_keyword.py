import googlemaps

def get_address(api_key,lat,lng):
    gmaps = googlemaps.Client(key=api_key)
    address = gmaps.reverse_geocode((lat,lng),language="ko")
    formatted_address = address[0].get("formatted_address")
    return formatted_address


def get_keyword(name,address):
    return address + " " + name
