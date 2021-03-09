import csv 
import numpy as np
import pycuda.driver as cuda
import math
import pycuda.autoinit
from pycuda.compiler import SourceModule
from distutils.util import strtobool
import time
import subprocess

def run_tsp(cities):
    comp = 'nvcc -std=c++11 -O3 -use_fast_math -arch=sm_61 ./utils_py/tsp/gpu_test.cu -o ./utils_py/tsp/gpu_test'
    tmp = subprocess.call(comp,shell=True) # OR gcc for c program
    #p = Popen(cmd,shell=True)
    print(f'num of {cities}')
    tmp = subprocess.call(args=['./utils_py/tsp/gpu_test', str(cities),'1','./utils_py/tsp/ig'])
    #tmp = subprocess.call(args=['./gpu_test',str(cities),'1','./ig'])
    with open('./utils_py/tsp/tsp_output.txt')as f:
        min_val = float(f.readline().split()[0])
        cycle_index =f.readline().split()
        cycle_index=list(map(int,cycle_index))
        return min_val,cycle_index


def tsp_cu(store_info):
  cities = len(store_info)
  return run_tsp(cities)
  

if __name__=="__main__":
    store_info = []
   
    with open('./ig') as readfile:
      row  = readfile.read().split('\n')
      row = [x for x in row if x != '']
      store_info = [i.split('@')for i in row]
      for i in store_info:
        i[1] = float(i[1])
        i[2] = float(i[2])
      #print(store_info)
    base_info = {
          'location' : "出發點",
          'latitude' : 24.796442,
          'longitude' : 120.996665, 
    }
    tsp_cu(store_info)
    
    #TSP(store_info,base_info)    
    