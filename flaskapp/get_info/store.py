
class Store(object):
    def __init__(self,name,formatted_address,icon,rating,reviews,types):
        self.__name = name
        self.__address = formatted_address
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


