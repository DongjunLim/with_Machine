import pymysql
#import mysqldb

class DB(object):
    def __init__(self,user_name,pw,language):
        self.__db = pymysql.connect(host='localhost',
                user=user_name.rstrip('\n'),
                password=pw.rstrip('\n'),
                db='withmachine',
                charset = 'utf8')
        self.__cursor = self.__db.cursor()
        self.__language = language
    def insert_store_table(self,sdata):

        store_sql = "INSERT INTO store (place_id,language,name,address,phone,price_level,rating) "
        store_sql += 'VALUES("{:}","{:}","{:}","{:}","{:}",{:},{:})'.format(sdata['place_id'],
                self.__language,
                sdata['name'],
                sdata['formatted_address'],
                sdata['phone'],
                sdata['price_level'],
                sdata['rating'])
        self.insert_db(store_sql)
        return

    def insert_reviews_table(self,sdata):
        for i in sdata['reviews']:
            
            reviews_sql = "INSERT INTO store_reviews (place_id,author_name, language, rating,relative_time,text) "
            reviews_sql += 'VALUES("{:}","{:}","{:}",{:},"{:}","{:}")'.format(sdata['place_id'],
                    i['author_name'],
                    self.__language,
                    i['rating'],
                    i['relative_time_description'],
                    i['text'])
            self.insert_db(reviews_sql)
        return

    def insert_types_table(self,sdata):
        for i in sdata['types']:
            print(i)
            types_sql = "INSERT INTO store_types (place_id,type) "
            types_sql += 'VALUES("{:}","{:}")'.format(sdata['place_id'],i)
            self.insert_db(types_sql)
        return
           
    def insert_db(self,sql):
        print(sql)
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
        except Exception as e:
            print(e)

    def close_db(self):
        if self.__db is not None:
            self.__db.close()

