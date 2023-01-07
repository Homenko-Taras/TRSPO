from mpi4py import MPI
import sys
import random
import math
from datetime import datetime

def isOnCircle(a,b,r):
    return math.sqrt(a*a+b*b)<=r

def Monte_Carlo(list):
    onCircle=0
    points=0
    for i,j in list:
        if(isOnCircle(i,j,1)):
            onCircle+=1
        points+=1
    return 4*onCircle/points

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ]



comm=MPI.COMM_WORLD
worker=comm.Get_rank()
size=comm.Get_size()

if(worker==0):
    arr=[]
    n=int(sys.argv[1])
    i=0
    while(i<n):
        arr.append((random.random(),random.random()))
        i+=1
    #print(arr)
    splits=split_list(arr,size)
    for i in range(1,size):
        splits[i].extend(splits[i-1])
else:
    splits=None
start_time=datetime.now()
data=comm.scatter(splits,root=0)
print (worker,Monte_Carlo(data),datetime.now()-start_time)
