class Cdata:
    def __init__(self,store_name,gps_lat,gps_lon,user_language,visit_language):
        self.__name = store_name
        self.__lat = gps_lat
        self.__lon = gps_lon
        self.__user_language = user_language
        self.__visit_language = visit_language
    def get_name(self):
        return self.__name
    def get_gps(self):
        return {
                'gps_lat' : self.__lat,
                'gps_lon' : self.__lon
                }
    def get_user_language(self):
        return self.__user_language
    def get_visit_language(self):
        return self.__visit_language

