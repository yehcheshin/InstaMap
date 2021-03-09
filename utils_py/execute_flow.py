from utils_py.class_decorators import *
from utils_py.main import *
from utils_py.map_mark import *

class TSP():
    def __init__(self):
        super().__init__()
        self.location = {"latitude":24.796349999865683, "longitude":120.99686002405213, "title" : "NTHU"}
        self.db_file = "./utils_py/store_from_DB.csv"
        self.radius = 0.9 #(line bot取得, default 500m)

    
    def execute_all(self):
        #使用者, 座標位置,名稱(line bot取得)
        #read_db_file = "./utils_py/store_from_DB.csv"
        base_info = [self.location["title"], self.location["latitude"], self.location["longitude"]]
        #print(base_info)
        #base_info = ['NTHU',24.796349999865683,120.99686002405213]
        #print(base_info)

        @tsp
        def tsp_cuda():
            return run_tsp_cu(self.db_file, self.radius, base_info)

        tsp_result, min_val = tsp_cuda()

        # get the html to AWS
        map_to_s3(tsp_result, self.radius)
        return "http://pl-instamap.s3-website-us-east-1.amazonaws.com", tsp_result

'''
def execute_all(base_info = None, radius = None):
    read_db_file = "./utils_py/store_from_DB.csv"
    base_info = ['NTHU',24.796349999865683,120.99686002405213] #使用者座標位置,名稱(line bot取得)
    radius = 0.9 #單位 公里 (line bot取得)

    @tsp
    def tsp_cuda():
        return run_tsp_cu(read_db_file, radius, base_info)

    tsp_result, min_val = tsp_cuda()

    # get the html to AWS
    map_to_s3(tsp_result, radius)
'''

if __name__=='__main__':
    t = TSP()
    url = t.execute_all() 
    print(url)
    #t.gogo()