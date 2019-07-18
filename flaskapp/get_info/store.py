
class Store(object):
    def __init__(self,name,address_components,icon,rating,reviews,types):
        self.__name = name
        self.__address = address_components
        self.__icon = icon
        self.__rating = rating
        self.__reviews = reviews
        self.__types = types

    def get_name(self):
        return self.__name
    def get_address(self):
        return self.__address
    def get_icon(self):
        return self.__icon
    def get_rating(self):
        return self.__rating
    def get_reviews(self):
        return self.__reviews
    def get_types(self):
        return self.__types

class Address(object):
    def __init__(self,floor,street_number,route,locality,admin_area_lv_2,
            admin_area_lv_1,country,postal_code):
        self.__floor = floor
        self.__street_number = street_number
        self.__route = route
        self.__locality = locality
        self.__admin_area_lv_2 = admin_area_lv_2
        self.__admin_area_lv_1 = admin_area_lv_1
        self.__country = country
        self.__postal_code = postal_code

    def get_floor(self):
        return self.__floor
    def get_street_number(self):
        return self.__street_number
    def get_route(self):
        return self.__route
    def get_locality(self):
        return self.__locality
    def get_admin_area_lv_2(self):
        return self.__admin_area_lv_2
    def get_admin_area_lv_1(self):
        return self.__admin_area_lv_1
    def get_country(self):
        return self.__country
    def get_postal_code(self):
        return self.__postal_code



class Review(object):
    def __init__(self):
        self.__author_name = author_name
        self.__author_url = author_url
        self.__profile_photo_url = profile_photo_url
        self.__rating = rating
        self.__relative_time_description = relative_time_description
        self.__text = text
        self.__time = time

    def get_author_name(self):
        return self.__author_name
    def get_author_url(self):
        return self,__author_url
    def get_profile_photo_url(self):
        return self.__profile_photo_url
    def get_rating(self):
        return self.__rating
    def get_relative_time_description(self):
        return self.__relative_time_description
    def get_text(self):
        return self.__text
    def get_time(self):
        return self.__time


