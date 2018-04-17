# coding=utf-8
import Preprocess
import Ridge
import bagproblem_B
import random

def RandomArray(day):
  array=[]
  for k in range(day):
    array.append(random.randint(0,1))
  return array
  

def length(n):
    if type(n)==int:
      return 1
    if type(n)!=int:
      count=0
      for index in enumerate(n):
        count=count+1
      return count
    
def div(array,n):
  for k in range(len(array)):
    array[k]=array[k]/n
  return array
  
  
def mean(array):#求数组array的均值
  meanvalue=0
  if len(array)!=0:
    meanvalue=sum(array)/len(array)
  return meanvalue
  
def dateToint(date):#为方便计算，将日期转化为整数，从0开始
    dateInt=[0]
    count=0;
    for index,item in enumerate(date):
      if date[index]!=date[-1]:
        if date[index]==date[index+1]:
          dateInt.append(count)
        if date[index]!=date[index+1]:
          count=count+1
          dateInt.append(count)
      if date[index]==date[-1]:
        break
    return dateInt
#计算输入date中每个日期的虚拟机个数，并返回一个顺序排序的数组
def numberofdate(date):
    number=1
    number_uu=[]
    count=0
    for index,item in enumerate(date):
        if index != length(date)-1:
          if date[index]==date[index+1]:
            number=number+1
          if date[index]!=date[index+1]:
            number_uu.append(number)
            count=count+1
            number=1
        if index == length(date)-1:
          if date[index-1]==date[index]:
            number_uu.append(number)
            count=count+1
          if date[index-1]!=date[index]:
            number_uu.append(1)
            count=count+1
    return number_uu,count

#计算对应虚拟机输入date中每个日期的虚拟机个数，并依次按照日期返回一个顺序排列的数组，若每一天虚拟机访问数量为0，将对应数组相应位置为0
def Numberofdate(date,flavor,Flavor):#flavor为虚拟机类型数组，Flavor为输入虚拟机类型
    if flavor[0]==Flavor:
      number=1
    if flavor[0]!=Flavor:
      number=0
    number_uu=[]
    for index,item in enumerate(date):
      if index != length(date)-1:
        if date[index]==date[index+1]:
          if flavor[index+1]==Flavor:
            number=number+1
        if date[index]!=date[index+1]:
          number_uu.append(number)
          if flavor[index+1]==Flavor:
            number=1
          if flavor[index+1]!=Flavor:
            number=0
      if index == length(date)-1:
        number_uu.append(number)
    return number_uu
def cal_date(createTime):
    date=[]
    time=[]
    for item in createTime:
        values=item.split(" ")
        date.append(values[0])
        time.append(values[1])
    return date,time
 
def predict0(number_uu,predictTime):#采用岭回归，预测值参与后续预测
    predict_result=[]
    x=[]
    mid=[]
    Len=len(number_uu)
    for k in range((Len-1)/2):
      mid=number_uu[k:k+Len/2]
      x.append(mid)
    y=number_uu[Len/2+1:]
    

    ridgeWeights = Ridge.ridgeRegres(x,y,200)
    for k in range(predictTime):       
      predict_value=Ridge.mulity(y[k:],ridgeWeights)
      if predict_value <= 0:
        predict_result.append(0)
      if predict_value > 0:
        if predict_value-int(predict_value)>=0.5:
          predict_result.append(int(predict_value)+1)
        if predict_value-int(predict_value)<0.5:
          predict_result.append(int(predict_value))
      y.append(predict_value)
    
    return predict_result
  
def predict1(number_uu,number_UU,predictTime):#采用岭回归，预测值不参与后续预测,number_UU表示总的虚拟机个数
    predict_result=[]
    #K=len(number_uu)/predictTime
    day=predictTime*2#注意边界问题
    for J in range(predictTime):
      x=[]
      mid=[]
      for k in range(len(number_uu)-day-J):
        mid=number_uu[k:k+day]
        for D in range(day):
          mid.append(number_UU[k+day])
        x.append(mid)
      y=number_uu[day+J:]
      ridgeWeights  = Ridge.ridgeRegres(x,y,90)#90(0-100取值内90最优)
      predict_x=[]
      predict_x=number_uu[len(number_uu)-day:]
      for D in range(day):
        predict_x.append(number_UU[len(number_uu)-day+D])
      predict_value=Ridge.mulity(predict_x,ridgeWeights)
      if predict_value <= 0:
        predict_result.append(0)
      if predict_value > 0:
        if predict_value-int(predict_value)>=0.5:
          predict_result.append(int(predict_value)+1)
        if predict_value-int(predict_value)<0.5:
          predict_result.append(int(predict_value))
    
    return predict_result


        
        
def predict2(number_uu,predictTime):#纯规则 均值
  predict_result=[]
  meanvalue=mean(number_uu)
  intvalue=int(meanvalue)
  for k in range(predictTime):
    predict_result.append(intvalue)
  return predict_result
  
def predict3(number_uu,predictTime):#预测方式3：直接选取每种类型的虚拟机后predictTime天作为预测结果
  predict_result=Ridge.add(number_uu[len(number_uu)-predictTime:],RandomArray(predictTime))
  return predict_result

  
def predict_vm(ecs_lines, input_lines):
    flavorName=[]
    createTime=[]
    number_uu=[]
    count=0#count代表总天数
    # Do your work from here#
    result = []
    if ecs_lines is None:
        print 'ecs information is none'
        return result
    if input_lines is None:
        print 'input file information is none'
        return result
      
    flavorName,createTime = Preprocess.Preprocess0(ecs_lines)
    #FlavorName,CreateTime = Preprocess.Preprocess1(ecs_lines)
    
    #按照cretTime将数组归类
    date=[]
    time=[]
    predict_Array={}
    predict_Array1={}#存储模型2
    date,time=cal_date(createTime)
    #print("各虚拟机随时间访问次数 flavor1-15")
    #number_uu数组为每日访问的虚拟机个数
    number_uu,count=numberofdate(date)
    number_uu1=Numberofdate(date,flavorName,'flavor1')
    #print(1,number_uu1,sum(number_uu1))
    number_uu2=Numberofdate(date,flavorName,'flavor2')
    #print(2,number_uu2,sum(number_uu2))
    number_uu3=Numberofdate(date,flavorName,'flavor3')
    #print(3,number_uu3,sum(number_uu3))
    number_uu4=Numberofdate(date,flavorName,'flavor4')
    #print(4,number_uu4,sum(number_uu4))
    number_uu5=Numberofdate(date,flavorName,'flavor5')
    #print(5,number_uu5,sum(number_uu5))
    number_uu6=Numberofdate(date,flavorName,'flavor6')
    #print(6,number_uu6,sum(number_uu6))
    number_uu7=Numberofdate(date,flavorName,'flavor7')
    #print(7,number_uu7,sum(number_uu7))
    number_uu8=Numberofdate(date,flavorName,'flavor8')
    #print(8,number_uu8,sum(number_uu8))
    number_uu9=Numberofdate(date,flavorName,'flavor9')
    #print(9,number_uu9,sum(number_uu9))
    number_uu10=Numberofdate(date,flavorName,'flavor10')
    #print(10,number_uu10,sum(number_uu10))
    number_uu11=Numberofdate(date,flavorName,'flavor11')
    #print(11,number_uu11,sum(number_uu11))
    number_uu12=Numberofdate(date,flavorName,'flavor12')
    #print(12,number_uu12,sum(number_uu12))
    number_uu13=Numberofdate(date,flavorName,'flavor13')
    #print(13,number_uu13,sum(number_uu13))
    number_uu14=Numberofdate(date,flavorName,'flavor14')
    #print(14,number_uu14,sum(number_uu14))
    number_uu15=Numberofdate(date,flavorName,'flavor15')
    #print(15,number_uu15,sum(number_uu15))
    
    #CPU_A为主机总的CPU核数，Mem_A为主机总的内存大小（G）,Num记录需要物理机的个数，N_A记录各虚拟机的存储情况
    CPU_A=0
    Mem_A=0
    Num_A=0
    N_A=[]
    inputArray={}
    for index,item in enumerate(input_lines):
      values = item.split(" ")
      inputArray[index]=values
    #读取主机的总CPU核数，和总内存大小
    CPU_A=int(inputArray[0][0])
    Mem_A=int(inputArray[0][1])
    #读取需要预测的虚拟机的种类和规格（CPU核数，内存大小）
    num_flavor=int(inputArray[2][0])
    flavor=[]
    CPU=[]
    Mem=[]
    for k in range(num_flavor):
      flavor.append(inputArray[3+k][0])#flavor存储需要预测的虚拟机种类
      CPU.append(inputArray[3+k][1])#CPU存储对应的CPU核数
      Mem.append(inputArray[3+k][2])#Mem存储对应的内存大小
    #读取需要优化的维度
    optimiDimension=inputArray[4+num_flavor]
    #读取需要预测的时间长度
    start_time=inputArray[6+num_flavor][0].split("-")
    end_time=inputArray[7+num_flavor][0].split("-")
    predict_time=int(end_time[2])-int(start_time[2])
    #预测部分：
    print("number_uu")
    print(number_uu)
    #print("虚拟机总数的预测")
    #predictArray=predict0(number_uu,predict_time)
    #print(predictArray)
    sumK=[]#存储flavor对应虚拟机的个数
    sumK1=[]
    sumK2=[]#存储对应flavor训练集每一天的均值*预测时间
    #number_predict1表示flavor1的预测
    for k in range(len(flavor)):
      if flavor[k]=='flavor1':
        predict_Array[k]=predict3(number_uu1,predict_time)
        sumK2.append(sum(number_uu1)*predict_time/len(number_uu1))
      if flavor[k]=='flavor2':
        predict_Array[k]=predict3(number_uu2,predict_time)
        sumK2.append(sum(number_uu2)*predict_time/len(number_uu1))
      if flavor[k]=='flavor3':
        predict_Array[k]=predict3(number_uu3,predict_time)
        sumK2.append(sum(number_uu3)*predict_time/len(number_uu1))
      if flavor[k]=='flavor4':
        predict_Array[k]=predict3(number_uu4,predict_time)
        sumK2.append(sum(number_uu4)*predict_time/len(number_uu1))
      if flavor[k]=='flavor5':
        predict_Array[k]=predict3(number_uu5,predict_time)
        sumK2.append(sum(number_uu5)*predict_time/len(number_uu1))
      if flavor[k]=='flavor6':
        predict_Array[k]=predict3(number_uu6,predict_time)
        sumK2.append(sum(number_uu6)*predict_time/len(number_uu1))
      if flavor[k]=='flavor7':
        predict_Array[k]=predict3(number_uu7,predict_time)
        sumK2.append(sum(number_uu7)*predict_time/len(number_uu1))
      if flavor[k]=='flavor8':
        predict_Array[k]=predict3(number_uu8,predict_time)
        sumK2.append(sum(number_uu8)*predict_time/len(number_uu1))
      if flavor[k]=='flavor9':
        predict_Array[k]=predict3(number_uu9,predict_time)
        sumK2.append(sum(number_uu9)*predict_time/len(number_uu1))
      if flavor[k]=='flavor10':
        predict_Array[k]=predict3(number_uu10,predict_time)
        sumK2.append(sum(number_uu10)*predict_time/len(number_uu1))
      if flavor[k]=='flavor11':
        predict_Array[k]=predict3(number_uu11,predict_time)
        sumK2.append(sum(number_uu11)*predict_time/len(number_uu1))
      if flavor[k]=='flavor12':
        predict_Array[k]=predict3(number_uu12,predict_time)
        sumK2.append(sum(number_uu12)*predict_time/len(number_uu1))
      if flavor[k]=='flavor13':
        predict_Array[k]=predict3(number_uu13,predict_time)
        sumK2.append(sum(number_uu13)*predict_time/len(number_uu1))
      if flavor[k]=='flavor14':
        predict_Array[k]=predict3(number_uu14,predict_time)
        sumK2.append(sum(number_uu14)*predict_time/len(number_uu1))
      if flavor[k]=='flavor15':
        predict_Array[k]=predict3(number_uu15,predict_time)
        sumK2.append(sum(number_uu15)*predict_time/len(number_uu1))
      sumK1.append(sum(predict_Array[k]))
    ######################################
    for k in range(len(flavor)):
      if flavor[k]=='flavor1':
        predict_Array1[k]=predict1(number_uu1,number_uu,predict_time)
      if flavor[k]=='flavor2':
        predict_Array1[k]=predict1(number_uu2,number_uu,predict_time)
      if flavor[k]=='flavor3':
        predict_Array1[k]=predict1(number_uu3,number_uu,predict_time)
      if flavor[k]=='flavor4':
        predict_Array1[k]=predict1(number_uu4,number_uu,predict_time)
      if flavor[k]=='flavor5':
        predict_Array1[k]=predict1(number_uu5,number_uu,predict_time)
      if flavor[k]=='flavor6':
        predict_Array1[k]=predict1(number_uu6,number_uu,predict_time)
      if flavor[k]=='flavor7':
        predict_Array1[k]=predict1(number_uu7,number_uu,predict_time)
      if flavor[k]=='flavor8':
        predict_Array1[k]=predict1(number_uu8,number_uu,predict_time)
      if flavor[k]=='flavor9':
        predict_Array1[k]=predict1(number_uu9,number_uu,predict_time)
      if flavor[k]=='flavor10':
        predict_Array1[k]=predict1(number_uu10,number_uu,predict_time)
      if flavor[k]=='flavor11':
        predict_Array1[k]=predict1(number_uu11,number_uu,predict_time)
      if flavor[k]=='flavor12':
        predict_Array1[k]=predict1(number_uu12,number_uu,predict_time)
      if flavor[k]=='flavor13':
        predict_Array1[k]=predict1(number_uu13,number_uu,predict_time)
      if flavor[k]=='flavor14':
        predict_Array1[k]=predict1(number_uu14,number_uu,predict_time)
      if flavor[k]=='flavor15':
        predict_Array1[k]=predict1(number_uu15,number_uu,predict_time)
      sumK.append(sum(predict_Array1[k]))
    #print("各虚拟机预测结果：")
    #print(predict_Array1)
    print("sumK2",sumK2)
    print("各虚拟机预测结果之和")
    c_array=[]
    for k1 in range(predict_time):
      c=0
      for k2 in range(len(flavor)):
        c=c+predict_Array[k2][k1]
      c_array.append(c)
    print(c_array)
    #求取预测的总数，并求其均值
    mean_line=mean(c_array)
    #平滑操作
    print("平滑前各虚拟机预测结果")
    print(sumK1)
    print("平滑前备选方案各虚拟机预测结果")
    print(sumK)
    meanvalue=mean(sumK1)  
    if meanvalue > 3 :
      for k in range(len(sumK1)):
        if sumK1[k] >= 3*meanvalue:
          sumK1[k]= meanvalue
        if sumK1[k] >= 2*meanvalue and sumK1[k] < 3*meanvalue:
          sumK1[k]= meanvalue
    #防止出现预测的sumK1全为0的情况
    if sum(sumK1) == 0:
      for k in range(len(sumK1)):
        sumK1[k]=1
    #所有的虚拟机在均线上下波动
    for k in range(len(sumK1)):
      sumK1[k]=sumK1[k]+mean_line/15+1
	for k in range(len(sumK1)/2):
      sumK1[k]=sumK1[k]+random.randint(0,2)
	
      
    meanvalue1=mean(sumK)  
    if meanvalue1 > 3 :
      for k in range(len(sumK)):
        if sumK[k] >= 3*meanvalue1:
          sumK[k]= meanvalue1
        if sumK[k] >= 2*meanvalue1 and sumK[k] < 3*meanvalue1:
          sumK[k]= meanvalue1
    #防止出现预测的sumK1全为0的情况
    if sum(sumK) == 0:
      for k in range(len(sumK)):
        sumK[k]=1
    #所有的虚拟机在均线上下波动
    for k in range(len(sumK)):
      sumK[k]=(sumK[k]+sumK1[k])/2
    print("平滑后备选方案各虚拟机预测结果")
    print(sumK)
    
    meanvalue2=mean(sumK2)  
    if meanvalue2 !=0 :
      for k in range(len(sumK2)):
        if sumK2[k] >= 3*meanvalue2:
          sumK2[k]= meanvalue2
        if sumK2[k] >= 2*meanvalue2 and sumK2[k] < 3*meanvalue2:
          sumK2[k]= meanvalue2/3
    if sum(sumK2) == 0:
      for k in range(len(sumK2)):
        sumK2[k]=1
    for k in range(len(sumK2)):
      sumK2[k]=sumK2[k]+mean_line/15
      
    Num_A,N_A=bagproblem_B.bagProblem(sumK1,CPU,Mem,CPU_A,Mem_A,optimiDimension)
    #print(Num_A)
    #print(N_A)
    result=[]
    result.append(sum(sumK1))
    for k in range(len(flavor)):
      b=""
      b=b+flavor[k]+" "+str(sumK1[k])
      result.append(b)
    result.append("")
    result.append(Num_A)
    for k in range(Num_A):
      a=""
      a=a+str(k+1)
      for k1 in range(len(flavor)):
        a=a+" "+flavor[k1]+" "+str(N_A[k][k1])
      result.append(a)
    return result

