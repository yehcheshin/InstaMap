import csv 
import numpy as np
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
from distutils.util import strtobool
import math

def kk():
  return "fun"

def get_dis(lat1, lon1, lat2, lon2):
    R = 6373
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

class dist():
  def __init__(self):
    self.read()
    self.cuda = cuda

  def read(self):
    location=[]
    target = []
    with open("raw_data.csv",newline='') as csvfile:
      rows = csv.reader(csvfile)
      for i,row in enumerate(rows):
        if i>=1:
          target.append(strtobool(row[1]))
          longitude= (row[0].strip("()").split(',')[0]) #[經度1,緯度1,經度2,緯度2.... ]
          latitude = (row[0].strip("()").split(',')[-1])
          location.append(longitude)
          location.append(latitude)
    
    self.location = location

  def allocate_mem(self):
    self.cuda.init()
    device = self.cuda.Device(0) # enter your gpu id here
    ctx = device.make_context()
    self.location= np.array(self.location,dtype=np.float64)
    self.length = np.int32(len(self.location))
    self.base = np.array([120.0000000,30],dtype=np.float64)
    self.resulted = np.empty((len(self.location)//2),dtype = np.float64)
    
    self.location_gpu = cuda.mem_alloc(self.location.nbytes)
    self.result_gpu = cuda.mem_alloc(self.resulted.nbytes)
    self.cuda.memcpy_htod(self.result_gpu,self.resulted)
    self.cuda.memcpy_htod(self.location_gpu,self.location)#int ratious,float* result,float * base
    self.base_gpu = cuda.mem_alloc(self.base.nbytes)
    self.cuda.memcpy_htod(self.base_gpu,self.base)
  

    self.mod = SourceModule("""
    #include <stdio.h>
    #include  <math.h>
    #define pi 3.1415926535897932384626433832795
    #define EARTH_RADIUS 6378.137
        __device__ double haversine (double lat1, double lon1, 
                                    double lat2, double lon2, double radius)
        {
        double dlat, dlon, c1, c2, d1, d2, a, c, t;

        c1 = cospif (lat1 / 180.0f);
        c2 = cospif (lat2 / 180.0f);
        dlat = lat2 - lat1;
        dlon = lon2 - lon1;
        d1 = sinpif (dlat / 360.0f);
        d2 = sinpif (dlon / 360.0f);
        t = d2 * d2 * c1 * c2;
        a = d1 * d1 + t;
        c = 2.0f * asinf (fminf (1.0f, sqrtf (a)));
        return radius * c;
        }
        
        __global__ void location_inrange(double *location_gpu, double *base, double *result, int length )
        { 
          
          int tid = threadIdx.x + blockDim.x * threadIdx.y;
          int i =  tid + blockDim.x * blockDim.y * blockIdx.x;
          if(i<length){
                double lat1 = location_gpu[i+i+1];
                double lon1 = location_gpu[i+i];
                result[i] = haversine (lat1, lon1, base[1], base[0], EARTH_RADIUS);
          }     
        }
    """)

    self.grid_size = int(self.length/16)
    self.func1 = self.mod.get_function("location_inrange")
    self.func1(self.location_gpu, self.base_gpu,self.result_gpu,self.length//2,block=(32,32,1),grid=(self.grid_size,1) )
    self.cuda.memcpy_dtoh(self.resulted, self.result_gpu)
    ctx.pop() 

    return self.resulted

if __name__ == '__main__':
  a = dist()
  