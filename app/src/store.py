class Store(object):
    def __init__(self,sdata):
        __place_id = " "
        __name = " "
        __address = " "
        __formatted_address = " "
        __rating = " "
        __price_level = " "
        __reviews = " "
        __types = " "
        __phone = " "
        __photos = " "
        for x in sdata:
            if x == 'place_id':
                self.__place_id = sdata['place_id']
            elif x == 'name':
                self.__name = sdata['name']
            elif x == 'address_components':
                self.__address = sdata['address_components']
            elif x == 'formatted_address':
                self.__formatted_address = sdata['formatted_address']
            elif x == 'rating':
                self.__rating = sdata['rating']
            elif x == 'price_level':
                self.__price_level = sdata['price_level']
            elif x == 'reviews':
                self.__reviews = sdata['reviews']
            elif x == 'types':
                self.set_type(sdata['types'])
            elif x == 'international_phone_number':
                self.__phone = sdata['international_phone_number']
            elif x == 'photos':
                self.__photo = sdata['photos']

    def set_type(self,types):
        
        if 'establishment' in types:
            types.remove('establishment')
        if 'point_of_interest' in types:
            types.remove('point_of_interest')
        
        self.__types = types
                


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
    def get_photo(self):
        return self.__photo
    def get_info(self):
        store_info = {
                'place_id':self.__place_id,
                'name':self.__name,
                'address':self.__address,
                'formatted_address':self.__formatted_address,
                'rating':self.__rating,
                'price_level':self.__price_level,
                'photo':self.__photo,
                'reviews' :self.__reviews,
                'types' :self.__types,
                'phone' :self.__phone
                }
        return store_info

