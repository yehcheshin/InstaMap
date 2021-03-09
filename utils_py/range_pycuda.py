import csv 
import numpy as np
import pycuda.driver as cuda
import math
import pycuda.autoinit
from pycuda.compiler import SourceModule
from distutils.util import strtobool

def in_range(store_info,base_info,radious):
    """
    使用pycuda計算範圍內店家
    """
    cuda.init()
    device = cuda.Device(0)
    ctx = device.make_context()
    latitude = np.array([i[1] for i in store_info])
    longitude = np.array([i[2] for i in store_info])

    num_store = len(store_info)
    base = np.array([base_info[1],base_info[2]],dtype=np.float64)
    resulted = np.empty((len(store_info)),dtype = np.float64)

    lat_gpu = cuda.mem_alloc(latitude.nbytes)
    lng_gpu = cuda.mem_alloc(longitude.nbytes)

    base_gpu = cuda.mem_alloc(base.nbytes)
    result_gpu = cuda.mem_alloc(resulted.nbytes)

    cuda.memcpy_htod(result_gpu,resulted)
    cuda.memcpy_htod(lat_gpu,latitude)
    cuda.memcpy_htod(lng_gpu,longitude)
    cuda.memcpy_htod(base_gpu,base)
    mod = SourceModule("""
    #include <stdio.h>
    #include  <math.h>
    #define pi 3.1415926535897932384626433832795
    #define EARTH_RADIUS 6378.137
        
    
        
        __global__ void get_location_inrange(double *latitude,double*longitude,double *base,double *result,int length )
        { 
        
        
        int threadId_2D = threadIdx.x + threadIdx.y*blockDim.x;
        int i = threadId_2D+ (blockDim.x*blockDim.y)*blockIdx.x;
        if(i<length){
            double radLat1,lat1,lng1;
            double radLat2,lat2,lng2;
            double a;
            double b;
            lat1=latitude[i];
            lat2=base[0];
            lng1=longitude[i];
            lng2=base[1];
            radLat1 =  lat1*pi/180.0 ;
            radLat2 =  lat2*pi/180.0;
            a = radLat1 -radLat2;
            b = lng1*pi/180.0 - lng2*pi/180.0;
            float s = 2 * asin(sqrt(pow(sin(a/2),2) + cos(radLat1)*cos(radLat2)*pow(sin(b/2),2)));
            s = s * EARTH_RADIUS;
            result[i] = s; //單位：公里

        }   
        }

    """)
    grid_size = math.ceil(num_store/1024)
    func1 = mod.get_function("get_location_inrange")
    func1(lat_gpu,lng_gpu,base_gpu,result_gpu,np.int32(num_store),block=(32,32,1),grid=(grid_size,1) )
    cuda.memcpy_dtoh(resulted,result_gpu)
    ctx.pop() 
    in_range_result = [store_info[i] for i,j in enumerate(resulted) if j<radious ]
    return in_range_result

def  store_txt(store_info):
    with open("./utils_py/tsp/ig",'w')as f:
        for row  in store_info:
            for i in row:
                if i != row[-1]:
                    f.write(str(i)+'@')
                else:
                    f.write(str(i))
            f.write('\n')

if __name__=='__main__':
    """
       result: data structure: list of list 
       功用:產生符合範圍內店家，並將result寫成txt檔 
    """
    store_info = []
    with open("./store_from_DB.csv",newline='') as csvfile:
        rows = csv.reader(csvfile)
        for i,row in enumerate(rows):
            if i>=1:
                row[1] = float(row[1])
                row[2] = float(row[2])
                store_info.append(row)
        

    base_info = ['NTHU',24.7961,120.9967] #使用者座標位置,名稱(line bot取得)
    radious = 0.5 #單位 公里 (line bot取得)
    store_info  = in_range(store_info,base_info,radious)
    tsp_info = [base_info]+store_info
    store_txt(tsp_info)
    