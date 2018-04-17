# -*- coding: utf-8 -*-
"""
Created on Mon Apr 09 20:17:59 2018

@author: pisoft
"""
import random
import Ridge
import predictor
import math
def zero(N):#构造一个长度为N的全零数组
  a=[]
  for k in range(N):
    a.append(0)
  return a
def calculateMem(N_A_N,Mem,Mem_A):
    result_mid=zero(len(Mem))
    mid3=0
    mid4=N_A_N[:]
    mid4.sort()
    
    mid1,mid2=predictor.numberofdate(mid4)
    for index,item in enumerate(mid1):
      mid3=mid3+item
      result_mid[N_A_N[mid3-1]]=item
    return float(Ridge.mulity(result_mid,Ridge.T(Mem)))/Mem_A

def restore(N_A_N,m,n):#返回将二维数组转化为一维数组对应元素的位置
  count=0
  for k1 in range(len(N_A_N)):
    if k1 != m:
      for k2 in range(len(N_A_N[k1])):
        count=count+1
    if k1 == m:
      for k2 in range(len(N_A_N[m])):
        if k2 != n:
          count=count+1
        else:
          return count
    
def Restore(N_A_N):#二维数组转为一维数组
  singe=[]
  for k1 in range(len(N_A_N)):
    for k2 in range(len(N_A_N[k1])):
      singe.append(N_A_N[k1][k2])
  return singe
  
      
def bagProblem(predict_Array,CPU,Mem,CPU_A,Mem_A,optimiDimension='MEM'):
  
  
  #对Mem,CPU进行相关处理
  for k1 in range(len(predict_Array)):
    Mem[k1]=int(Mem[k1])/1024
    CPU[k1]=int(CPU[k1]) 
  Num_R=predict_Array[:]#记录每种虚拟机的剩余数量
  M=len(Mem)
  
  N_A_NBest=[]
  array=[]
  
  print('--------------')
  print('内存')
  print(Mem)
  print('CPU')
  print(CPU)
  print("预测各虚拟机个数")
  print(Num_R)
  print("主机CPU")
  print(CPU_A)
  print("主机内存")
  print(Mem_A)
  print("优化资源维度")
  print(optimiDimension)
  print('--------------')
  print("模拟退火算法寻求最优解")
  for k1 in range(M):
    for k2 in range(Num_R[k1]):
      array.append(k1)
#  print(array,len(array))
  #array=array1[:]
  min_score=M#记录最高得分
  score=0
  T=1000
  r=0.9999
  N_A_N=[]
  while T>1:
    Num_A=1#记录主机的个数
    Num=sum(Num_R)
    if T < 1000:
      m2=random.randint(0,len(N_A_N)-1)
      n2=random.randint(0,len(N_A_N)-1)
      m1=random.randint(0,len(N_A_N[m2])-1)
      n1=random.randint(0,len(N_A_N[n2])-1)
      switch1=restore(N_A_N,m2,m1)
      switch2=restore(N_A_N,n2,n1)
    if T == 1000:
      switch1=0
      switch2=0
    
    N_A_N=[]#记录每个主机所能容纳的虚拟机的分配情况
    
    newarray=array[:]
    #交换操作
    mid=newarray[switch1]
    newarray[switch1]=newarray[switch2]
    newarray[switch2]=mid
    
    
    Mem_U=[]#记录每个主机所剩余的Mem总数
    CPU_U=[]#记录每个主机所剩余的CPU总数
    m=0#断点
    n=0#计数
    #首次适应法
    while Num > 0:
      #新建一个主机
      Mem_R=Mem_A#主机剩余的Mem
      CPU_R=CPU_A#主机剩余的CPU个数
      N_A=[]#记录主机上所能容纳的各虚拟机的个数，长度为虚拟机的种类

      for k in newarray[m:]:
        if Mem[k] <= Mem_R and CPU[k] <= CPU_R:
          Num=Num-1
          N_A.append(k)
          Mem_R=Mem_R-Mem[k]
          CPU_R=CPU_R-CPU[k]
          if Num==0:
            N_A_N.append(N_A)
            
            break
          n=n+1
        if Mem_R <= 0 or CPU_R <= 0 or Mem[k] > Mem_R or CPU[k] > CPU_R:
          Mem_U.append(Mem_R)
          CPU_U.append(CPU_R)
          N_A_N.append(N_A)
          m=n
          
          break
      Num_A=Num_A+1
    #print(Mem_U,CPU_U,N_A_N)
    #当最后一个主机分配的虚拟机个数少于3个的时候，尝试将后一个主机的虚拟机分配给前面主机：
    c=0
    
    if len(N_A_N[-1]) <= M/3:
      
      for k1 in range(len(N_A_N[-1])):
        for k2 in range(len(N_A_N)-1):
          if Mem_U[k2] >= Mem[N_A_N[-1][k1]] and CPU_U[k2] >= CPU[N_A_N[-1][k1]] and N_A_N[-1][k1] != 100:
            N_A_N[k2].append(N_A_N[-1][k1])
            Mem_U[k2] = Mem_U[k2]-Mem[N_A_N[-1][k1]]
            CPU_U[k2] = CPU_U[k2]-CPU[N_A_N[-1][k1]]
            N_A_N[-1][k1]=100
            c=c+1
            break
      for k1 in range(c):
        N_A_N[-1].remove(100)
      if len(N_A_N[-1])==0:
        N_A_N.remove(N_A_N[-1])
      newarray=Restore(N_A_N)
    
            
            
            
    if optimiDimension==['MEM\n']:
      score=len(N_A_N)-1+calculateMem(N_A_N[-1],Mem,Mem_A)
    else:
      score=len(N_A_N)-1+calculateMem(N_A_N[-1],CPU,CPU_A)
    if score<min_score:
      min_score=score
      array=newarray[:]
      N_A_NBest=N_A_N[:]
    else:
      if math.exp((min_score-score)/T) > random.random():
        min_score=score
        N_A_NBest=N_A_N[:]
        array=newarray[:]
    T=T*r
    
  Num_A1=len(N_A_NBest)  
  print(N_A_NBest,min_score,Num_A1)
  result=[]   
  for k1 in range(len(N_A_NBest)):
    result_mid=zero(M)
    mid3=0
    mid4=N_A_NBest[k1]
    mid4.sort()
    
    mid1,mid2=predictor.numberofdate(mid4)
    for index,item in enumerate(mid1):
      mid3=mid3+item
      result_mid[N_A_NBest[k1][mid3-1]]=item
    result.append(result_mid)
  print(result)
  for k in range(len(result)):
    print(Ridge.mulity(result[k],Ridge.T(CPU)))
    print(Ridge.mulity(result[k],Ridge.T(Mem)))
  return Num_A1,result
      
    
  
      
        
        
          
    
      
      
    
  
  
