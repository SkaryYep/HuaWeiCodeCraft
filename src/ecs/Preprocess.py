# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 15:38:16 2018

@author: pisoft
"""
def judge(flavorName):
    if flavorName=='flavor1' or flavorName=='flavor2' or flavorName=='flavor3' or flavorName=='flavor4' or flavorName=='flavor5' or flavorName=='flavor6' or flavorName=='flavor7' or flavorName=='flavor8' or flavorName=='flavor9' or flavorName=='flavor10' or flavorName=='flavor11' or flavorName=='flavor12' or flavorName=='flavor13' or flavorName=='flavor14' or flavorName=='flavor15' :
      return True
    else:
      return False
def Preprocess0(ecs_lines):
    #预处理：去除多余的虚拟机
    flavorName=[]
    createTime=[]
    for index, item in enumerate(ecs_lines):
        values = item.split("\t")
        if judge(values[1]):
          flavorName.append(values[1])
          createTime.append(values[2])
    return flavorName,createTime
def Preprocess1(ecs_lines):
    #预处理：不仅去除多余的虚拟机，并且将每个虚拟机分类，按照时间生成单个虚拟机请求数量随时间变化的数组
    flavorName1=[];flavorName2=[];flavorName3=[];flavorName4=[];flavorName5=[];flavorName6=[];flavorName7=[];flavorName8=[];flavorName9=[];flavorName10=[];flavorName11=[];flavorName12=[];flavorName13=[];flavorName14=[];flavorName15=[];
    createTime1=[];createTime2=[];createTime3=[];createTime4=[];createTime5=[];createTime6=[];createTime7=[];createTime8=[];createTime9=[];createTime10=[];createTime11=[];createTime12=[];createTime13=[];createTime14=[];createTime15=[];
    flavorName={};createTime={}
    for index, item in enumerate(ecs_lines):
        values = item.split("\t")
        if values[1] == 'flavor1':
          flavorName1.append(values[1])
          createTime1.append(values[2])
        if values[1] == 'flavor2':
          flavorName2.append(values[1])
          createTime2.append(values[2])
        if values[1] == 'flavor3':
          flavorName3.append(values[1])
          createTime3.append(values[2])
        if values[1] == 'flavor4':
          flavorName4.append(values[1])
          createTime4.append(values[2])
        if values[1] == 'flavor5':
          flavorName5.append(values[1])
          createTime5.append(values[2])
        if values[1] == 'flavor6':
          flavorName6.append(values[1])
          createTime6.append(values[2])
        if values[1] == 'flavor7':
          flavorName7.append(values[1])
          createTime7.append(values[2])
        if values[1] == 'flavor8':
          flavorName8.append(values[1])
          createTime8.append(values[2])
        if values[1] == 'flavor9':
          flavorName9.append(values[1])
          createTime9.append(values[2])
        if values[1] == 'flavor10':
          flavorName10.append(values[1])
          createTime10.append(values[2])
        if values[1] == 'flavor11':
          flavorName11.append(values[1])
          createTime11.append(values[2])
        if values[1] == 'flavor12':
          flavorName12.append(values[1])
          createTime12.append(values[2])
        if values[1] == 'flavor13':
          flavorName13.append(values[1])
          createTime13.append(values[2])
        if values[1] == 'flavor14':
          flavorName14.append(values[1])
          createTime14.append(values[2])
        if values[1] == 'flavor15':
          flavorName15.append(values[1])
          createTime15.append(values[2])
    flavorName[0]=flavorName1;flavorName[1]=flavorName2;flavorName[2]=flavorName3;flavorName[3]=flavorName4;flavorName[4]=flavorName5;flavorName[5]=flavorName6;flavorName[6]=flavorName7;flavorName[7]=flavorName8;flavorName[8]=flavorName9;flavorName[9]=flavorName10;flavorName[10]=flavorName11;flavorName[11]=flavorName12;flavorName[12]=flavorName13;flavorName[13]=flavorName14;flavorName[14]=flavorName15;
    createTime[0]=createTime1;createTime[1]=createTime2;createTime[2]=createTime3;createTime[3]=createTime4;createTime[4]=createTime5;createTime[5]=createTime6;createTime[6]=createTime7;createTime[7]=createTime8;createTime[8]=createTime9;createTime[9]=createTime10;createTime[10]=createTime11;createTime[11]=createTime12;createTime[12]=createTime13;createTime[13]=createTime14;createTime[14]=createTime15;
    return flavorName,createTime
  

    
