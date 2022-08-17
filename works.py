from operator import index
from pickle import TRUE
import pandas as pd
import matplotlib.pyplot as plt

def trim_CSV(merged_path,idle_time,col_name):
    to_trim = pd.read_csv(merged_path)
    print(col_name)
    count=0
    initialZeroFlag = 0
    initialZero = 0
    nextZero = 0
    total = 0
    arr = [0]*1000
    j=0
    ZCount = 0
    greater = 0
    average = 0
    highest = 0
    lowest = 200
    sample = 0
    option = 'TS'
    if option == 'TS':
        for i in range(len(to_trim)):
            if(to_trim.loc[i,col_name] == 0 and initialZeroFlag == 0):
                initialZeroFlag = 1
                initialZero = i
                count = count+1
            elif(to_trim.loc[i,col_name] == 0):
                count = count + 1
            elif(to_trim.loc[i,col_name] != 0 and initialZeroFlag != 0):
                nextZero = i
                if(count>int(idle_time)):
                    arr[j] = initialZero
                    arr[j+1] = nextZero
                    j = j+2
                    count=0
                    initialZeroFlag =0
                if(count<int(idle_time)):
                    initialZeroFlag =0
                    count=0         
        arr[j] = 1111.1111
        j=0

        while(arr[j]!= 1111.1111):
            total = total+1
            j = j + 1

        arr1 = [0]*total
        j=0

        while(j<total):
            arr1[j] = arr[j]
            j = j + 1

        j=0
        toMinus = 0

        while(j<total):
            to_trim.drop(to_trim.index[arr1[j]-toMinus:arr1[j+1]-toMinus],0,inplace = True)
            toMinus = toMinus + (arr1[j+1] - arr1[j])
            j=j+2

    to_trim = to_trim.reset_index(drop=True)
    print(to_trim.info())
    to_trim.to_csv(merged_path,index = False)
    to_trim = pd.read_csv(merged_path)
    print(to_trim.info())
    return merged_path

def plot_csv(filePath,xAxis,yAxis,heading):
    to_plot = pd.read_csv(filePath)
    fig = plt.figure(figsize=(7,4))
    plt.plot(linewidth = '.02')
    plt.plot(to_plot,label = "plot 1")
    plt.title(heading)
    plt.xlabel(xAxis)
    plt.ylabel(yAxis)
    fig.savefig('./static/plot1.jpg',dpi = 500)
    print("plot csv works")

def details_csv(file_path):
    print("details call success")

def getColName(df):
    cols = df.columns
    return cols

def removeRows(csv_path,option,strt_stp,time,file_name):
    print(csv_path)
    print(option)
    print(strt_stp)
    print(time)
    df = pd.read_csv(csv_path)
    if(option == 'remove'):
        if(strt_stp == 'fromStart' and int(time) > 0):
            df.drop(df.index[0:int(time)],0,inplace = True)
            print("Dropped")
        if(strt_stp == 'fromEnd' and int(time) >= 0):
            df.drop(df.index[df.shape[0] - int(time) : df.shape[0]],0,inplace = True)
    print(df.info())
    print(file_name)
    file_path = './files/' + file_name
    print(file_path)
    df.to_csv(file_path,index = False)

def removeRowsFromStart(filePath,time):
    print("Remove rows from start called")
    df = pd.read_csv(filePath)
    df.drop(df.index[0:int(time)] , 0 , inplace= True)
    print(df.info())
    df.to_csv(filePath,index=False)
    return filePath

def removeRowsFromMiddle(filePath,fromTime,toTime):
    print("Remove Rows From Middle")
    df = pd.read_csv(filePath)
    df.drop(df.index[int(fromTime):int(toTime)+1] , 0 , inplace = True)
    print(df.info())
    df.to_csv(filePath,index=False)
    return filePath

def removeRowsFromEnd(filePath,time):
    print("Remove From End Called")
    df = pd.read_csv(filePath)
    df.drop(df.index[df.shape[0]-int(time) : df.shape[0]], 0, inplace = True)
    print(df.info())
    df.to_csv(filePath,index=False)
    return filePath

def deleteColumn(file,filePath,columnName):
    df = pd.read_csv(filePath)
    print(df.info())
    print(columnName)
    df.drop(columnName,axis=1,inplace=True)
    print(df.info())
    df.to_csv(filePath,index=False)

def checkColumnPresent(filePath,columnName):
    isPresent = 0
    df = pd.read_csv(filePath)
    for col in df.columns:
        if col == columnName:
            isPresent = 1
    if isPresent == 1:
        return 1
    else:
        return 0
    
def resetCol(filePath,colName):
    df = pd.read_csv(filePath)
    print(len(df))
    df = df.reset_index(drop=True)
    for i in range(len(df)):
        df.loc[i,colName] = i
    df.to_csv(filePath,index=False)
    
def changeColumnName(filePath,oldName,newName):
    print(filePath)
    print(oldName)
    print(newName)
    df = pd.read_csv(filePath)
    print(df.info())
    df = df.rename(columns={oldName:newName})
    print(df.info())
    df.to_csv(filePath,index=False)

def changeIndexColumn(filePath,columnName):
    df = pd.read_csv(filePath)
    df = df.set_index(columnName)
    print(df.info())
    df.to_csv(filePath,index=False)
    
