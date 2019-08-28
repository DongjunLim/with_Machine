import pandas as pd
import json
pd.set_option('display.max_colwidth', -1)

class csv_data:

    def toJSON(self):
        return self.__dict__
        #return json.dumps(self, default=lambda o: o.__dict__,
         #                 sort_keys=True, indent=4)
    def make_list(lines):
        b=lines.replace("[[","").replace("]]","")
        matrixAr = []
        for line in b.split('], ['):
            line = line.replace("'", "")
            if(line.split(',')):
                row =list(map(str,line.split(',')))
            else:
                row = list(line)
            matrixAr.append(row)
        #print("mat[0]" ,matrixAr[0])
        return matrixAr

    def __init__(self, name):
        data_frame = pd.read_csv("/home/ubuntu/server/app/src/get_info/TA_restaurants_curated.csv", )
        # Name 컬럼??서 가?????름??검??(data_row ????
        value = data_frame.loc[data_frame['Name'].str.contains(name)]

       #self.city = value['City'].to_string(index=False)
        self.csv_type = value['Cuisine Style'].to_string(index=False)[2:-1]
        #self.rank = value['Ranking'].to_string(index=False)
        self.csv_rating = value['Rating'].to_string(index=False)
        self.csv_Prank = value['Price Range'].to_string(index=False)
        self.csv_reviews =  csv_data.make_list(value['Reviews'].to_string(index=False))[0]
        # print("self.type = ", self.reviews[0])
        

        # csv??서 ??정 ????택 ?? ?????에????요????이??만 추출
# result = csv_data()
# print(result.toJSON())

# ??요??리뷰???추출





