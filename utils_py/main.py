from utils_py.range_pycuda import in_range,store_txt
from utils_py.tsp.tsp_pycuda import tsp_cu
import csv
# import map_mark

def run_tsp_cu(read_db_file, radius, base_info):
    """
       result: data structure: list of list 
       功用:產生符合範圍內店家，並將result寫成txt檔 
    """
    store_info = []
    with open(read_db_file, newline='') as csvfile:
        rows = csv.reader(csvfile)
        for i,row in enumerate(rows):
            if i>=1:
                row[1] = float(row[1])
                row[2] = float(row[2])
                store_info.append(row)
        
    result = in_range(store_info, base_info, radius)
    tsp_info = [base_info] + result
    store_txt(tsp_info)
    min_val,cycle = tsp_cu(tsp_info)
    tsp_result = []
    for index,i in enumerate(cycle):
        if i == 0:
            offset = index
    if offset!=0:        
        left = cycle[:offset+1]
        right = cycle[offset:-1]
        cycle = right+left

    for i in cycle:
        tsp_result.append(tsp_info[i])
  
    return tsp_result, min_val


if __name__=='__main__':
    """
       result: data structure: list of list 
       功用:產生符合範圍內店家，並將result寫成txt檔 
    """

    read_db_file = "./store_from_DB.csv"
    base_info = ['NTHU',24.796349999865683,120.99686002405213] #使用者座標位置,名稱(line bot取得)
    radius = 0.1 #單位 公里 (line bot取得)

    tsp_result, min_val = run_tsp_cu(read_db_file, radius, base_info)
    '''
    store_info = []
    with open("./store_from_DB.csv",newline='') as csvfile:
        rows = csv.reader(csvfile)
        for i,row in enumerate(rows):
            if i>=1:
                row[1] = float(row[1])
                row[2] = float(row[2])
                store_info.append(row)
        

    base_info = ['NTHU',24.796349999865683,120.99686002405213] #使用者座標位置,名稱(line bot取得)
    radius = 0.1 #單位 公里 (line bot取得)
    result = in_range(store_info,base_info,radius)
    tsp_info = [base_info] + result
    store_txt(tsp_info)
    min_val,cycle = tsp_cu(tsp_info)
    tsp_result = []
    for index,i in enumerate(cycle):
        if i==0:
            offset = index
    if offset!=0:        
        left = cycle[:offset+1]
        right = cycle[offset:-1]
        cycle = right+left
  
    

    for i in cycle:
        tsp_result.append(tsp_info[i])
    '''
        
    
    print("TSP : min cost {} km".format(min_val))
    print(tsp_result)
    #map_mark(tsp_result)
    
    
    
    