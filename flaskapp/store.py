class Store(object):
    def __init__(self,sdata):
        self.__place_id = sdata['place_id']
        self.__name = sdata['name']
        self.__address = sdata['address_components']
        self.__formatted_address = sdata['formatted_address']
        self.__rating = sdata['rating']
        self.__price_level = sdata['price_level']
        self.__reviews = sdata['reviews']
        self.__types = sdata['types']
        self.__phone = sdata['international_phone_number']
        self.__photos = sdata['photos']
    def get_name(self):
        return self.__name
    def get_address(self):
        return self.__address
    def get_rating(self):
        return self.__rating
    def get_reviews(self):
        return self.__reviews
    def get_types(self):
        return self.__types
    def get_info(self):
        store_info = {
                'place_id':self.__place_id,
                'name':self.__name,
                'address':self.__address,
                'formatted_address':self.__formatted_address,
                'rating':self.__rating,
                'price_level':self.__price_level,
                'reviews' :self.__reviews,
                'types' :self.__types,
                'phone' :self.__phone
                }
        print(store_info)
        return store_info


data = {
        'place_id':'armada55',
        'name': 'conhas',
        'address_components' : 'yeonhee',
        'formatted_address' : 'seogyo',
        'rating' : 5.0,
        'price_level' : 1.0,
        'reviews' : {
            'author_name' : 'dongjun',
            'text' : 'Its good place',
            },
        'types' : 'cafe',
        'international_phone_number' : '010-9120-7304',
        'photos' : 'refer'
        }


store = Store(data)
store.get_info()

