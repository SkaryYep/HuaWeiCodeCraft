# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 16:17:54 2018

@author: pisoft
"""
##使用岭回归进行预测
def length(n):
    if type(n)==int or type(n)==float:
      return 1
    else:
      count=0
      for index in enumerate(n):
        count=count+1
      return count
def add(x,y):#矩阵元素相加
  z=[];
  mid=[];
  if length(x[0])==1:
    for k in range(len(x)):
      z.append(x[k]+y[k])
  else:
    for k1 in range(len(x)):
      for k2 in range(len(x[0])):
        mid.append(x[k1][k2]+y[k1][k2])
      z.append(mid)
      mid=[]
  return z
              
def T(Array):#转置函数
  Len=len(Array)
  wide=length(Array[0])
  if Len==1:
    return Array
  if wide==1:
    if type(Array[0])==int or type(Array[0])==float:
      Array_new=[]
      mid=[]
      for k in range(Len):
        mid.append(Array[k])
        Array_new.append(mid)
        mid=[]
      return Array_new
    if type(Array[0])!=int and type(Array[0])!=float:
      Array_new=[]
      for k in range(Len):
        Array_new.append(Array[k][0])
      return Array_new
  if Len !=1 and wide != 1:
    Array_new=[]
    mid=[]
    for k1 in range(wide):
      for k2 in range(Len):
        mid.append(Array[k2][k1])
      Array_new.append(mid)
      mid=[]
    return Array_new 
def vectorMulity(a,b):#两个向量做内积
  if len(a) == 1:
    return a[0]*b[0]
  if len(a) != 1:
    mid=0
    result=0
    for k in range(len(a)):
      mid=a[k]*b[k]
      result=result+mid
    return result
  
def mulityInt(data,a):#矩阵与数相乘：
  for k1 in range(len(data)):
    for k2 in range(length(data[0])):
      data[k1][k2]=data[k1][k2]*a
  return data

def mulity(a,b):#矩阵相乘,目前对于行或列为1的矩阵存在问题
  aLen=len(a)
  bLen=len(b)
  bT=T(b)
  if length(bT[0])==1:
    bT=[bT]
  bTLen=len(bT)
  if aLen==1 and bLen==1:
    return a[0]*b[0]
  if length(a[0])==1:
    return vectorMulity(a,bT[0])
  if length(a[0])!=1:
    mid=[]
    midArray=[]
    for k1 in range(aLen):
      for k2 in range(bTLen):
        mid.append(vectorMulity(a[k1],bT[k2]))
      midArray.append(mid)
      mid=[]
    return midArray
     
      
def eye(N):#单位函数
  eyeA=[]
  eyeB=[]
  for k1 in range(N):
    for k2 in range(N):
      eyeA.append(0)
    eyeB.append(eyeA)
    eyeA=[]
  for k1 in range(N):
    eyeB[k1][k1]=1
  return eyeB    

def shape(Array):#返回矩阵的行列数，数组中第一个元素为行数，第二个元素为列数
  result=[]
  if type(Array[0]) == int or type(Array[0]) == float :
    result.append(1)
    result.append(length(Array))
  if type(Array[0]) != int and type(Array[0]) != float:
    result.append(len(Array))
    result.append(len(Array[0]))
  return result

def swap(Input,output,target,source):
  if target==source:
    return 0
  a=Input[target]
  b=output[target]
  Input[target]=Input[source]
  Input[source]=a
  output[target]=output[source]
  output[source]=b

 
def copy(matrix):#实现二维矩阵深拷贝功能
  matrix_copy=[]
  mid=[]
  for k1 in range(len(matrix)):
    for k2 in range(len(matrix[0])):
      mid.append(matrix[k1][k2])
    matrix_copy.append(mid)
    mid=[]
  return matrix_copy
  
def inverseMatrix(Matrix):
  matrix=copy(Matrix)
  Len=len(matrix)
  if Len!=length(matrix[0]):
    print("matrix is not a squared matrix ! ")
  #caucalate a uit matrix
  res=eye(Len)
  for i in range(Len):#i代表列
    for j in range(Len):
      if matrix[j][i] !=0:
        if j!=0:
          swap(matrix,res,0,j)
        break
    for j in range(Len):
      if j==0:
        for k in range(Len-1,-1,-1):
          res[j][k] = float(res[j][k]) / matrix[j][i]
        for k in range(Len-1,i-1,-1):
          matrix[j][k] /= float(matrix[j][i])
      else:
        for k in range(Len-1,-1,-1):
          res[j][k] = res[j][k] - float(matrix[j][i]) / matrix[0][i] * res[0][k]
        for k in range(Len-1,i-1,-1):
          matrix[j][k] = matrix[j][k] - float(matrix[j][i]) / matrix[0][i] * matrix[0][k]
    swap(matrix, res, 0, (i + 1) % Len);  #交换需要进行变化的一行到第一行
  for k in range(Len-1):
    swap(matrix,res,k,k+1)
  #swap(matrix, res, 0, Len - 1)
  
  return res
 




      



#岭回归
def ridgeRegres(xMat,yMat,lam=0.2):  
    xTx = mulity(T(xMat),xMat)  
    denom = add(xTx , mulityInt(eye(shape(xMat)[1]),lam))  
    ws = mulity(inverseMatrix(denom) ,mulity(T(xMat),T(yMat)))  
    return ws  

def ridgeTest(xArr,yArr):  
    xMat = np.mat(xArr); yMat=T(np.mat(yArr))  
    yMean = np.mean(yMat) # 数据标准化  
    # print(yMean)  
    yMat = yMat - yMean  
    print(xMat)  
    #regularize X's  
    xMeans = np.mean(xMat,0)  
    xVar = np.var(xMat,0)  
    xMat = (xMat - xMeans) / xVar #（特征-均值）/方差  
    numTestPts = 30  
    wMat = np.zeros((numTestPts,shape(xMat)[1]))  
    print(xMat)
    print(yMat)
    for i in range(numTestPts): # 测试不同的lambda取值，获得系数  
        ws = ridgeRegres(xMat,yMat,np.exp(i-10))  
        wMat[i,:]=T(ws)  
    return wMat  

# import data  
#x=[]
#mid=[]
#for k in range(21):
#  mid=number_uu[k:k+21]
#  x.append(mid)
#y=number_uu[21:]  

#ridgeWeights = ridgeRegres(xArr,yArr,0.2)  
#y_predict=mulity(x,ridgeWeights)
