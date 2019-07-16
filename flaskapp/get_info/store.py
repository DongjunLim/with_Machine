
class store(object):
    def __init__(self):
        self.__name = name
        self.__address_components = address_components
        self.__icon = icon
        self.__rating = rating
        self.__reviews = reviews
        self.__types = types

class address_components(object):
    def __init__(self):
        self.__floor = floor
        self.__street_number = street_number
        self.__route = route
        self.__locality
        self.__admin_area_lv_2
        self.__admin_area_lv_1
        self.__country
        self.__postal_code

class review(object):
    def __init__(self):
        self.__author_name = author_name
        self.__author_url = author_url
        self.__profile_photo_url = profile_photo_url
        self.__rating = rating
        self.__relative_time_description = relative_time_description
        self.__text = text
        self.__time = time

