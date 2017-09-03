#!/usr/bin/python
# -*- coding: UTF-8 -*-
from os import listdir
from os.path import isfile, join
import os
import Queue
import threading
import time

pubFileQueue = Queue.Queue()
preLogList = []

#得到log文件夹下的日志文件
def getFileListFromDirectory(directory):
    onlyfiles = [ directory + '/' + f for f in listdir(directory) if isfile(join(directory,f)) ]
    return onlyfiles

def sameSuccessiveMemberCount(memberList, width):
    arrowRight = '---->'
    size = len(memberList)
    # print size # this is a test
    i = 0
    resultList = []
    limitPosition = size - width
    while i <= limitPosition:
        parten = memberList[i : i + width]
        count = 1
        j = i + width
        nextToCmp = memberList[j : j + width]
        while parten == nextToCmp:
            count += 1
            j += width
            nextToCmp = memberList[j : j + width]
        if count > 1:
            temp = '['
            for x in xrange(width):
                if x == 0:
                    temp += parten[x]
                else:
                    temp = temp + arrowRight + parten[x]
            temp += ', ' + str(count) + ']'
            resultList.append(temp)
            i = j
        else:
            resultList.append(memberList[i])
            i += 1
    while i < size:
        resultList.append(memberList[i])
        i += 1
    return resultList

def merge(memberList):
    size = len(memberList)
    limit = size / 2
    width = 1
    preResultList = memberList
    resultList = sameSuccessiveMemberCount(preResultList, width)
    while width <= limit:
        if resultList == preResultList:
            width += 1
        else:
            preResultList = resultList
        resultList = sameSuccessiveMemberCount(preResultList, width)
    return resultList


def output2(statisticsResult, resultPath):
    #filename = resultPath + '\\' + filePath.split('\\').pop() + '.log'
    f = open(resultPath, 'a')
    count = len(statisticsResult)
    if count >0:
        index = 0
        arrowRight = '---->'
        for i in xrange(count):
            if i == count - 1:
                f.write(statisticsResult[i])
            else:
                f.write(statisticsResult[i] + arrowRight)
            index += 1
            if index == 3:
                f.write(os.linesep)
                index = 0
    f.write(os.linesep + '-' * 100 + os.linesep)
    f.close()

def filterMember(arrayLine, filename, newFileName):
    syscallNumber = arrayLine[0]
    item = ''
    if syscallNumber == '52':
        syscallName = 'NtCreateFile'
        createDisposition = arrayLine[4]
        item = syscallName + '(' + filename + ', ' + createDisposition + ')'
    if syscallNumber == '30':
        syscallName = 'NtOpenFile'
        item = syscallName + '(' + filename + ')'
    if syscallNumber == '5':
        syscallName = 'NtWriteFile'
        bufferLength = arrayLine[5]
        item = syscallName + '(' + filename + ', ' + bufferLength + 'B)'
    if syscallNumber == '48':
        syscallName = 'FlushBuffersFile'
        item = syscallName + '(' + filename + ')'
    if syscallNumber == '18d':
        syscallName = 'NtWriteFileGather'
        item = syscallName + '(' + filename + ')'
    if syscallNumber == '3':
        syscallName = 'NtReadFile'
        bufferLength = arrayLine[5]
        item = syscallName + '(' + filename + ', ' + bufferLength + 'B)'
    if syscallNumber == '112':
        syscallName = 'NtReadFileScatter'
        item = syscallName + '(' + filename + ')'
    if syscallNumber == 'b2':
        syscallName = 'NtDeleteFile'
        item = syscallName + '(' + filename + ')'
    if syscallNumber == '24':  
        if newFileName == '':
            syscallName = 'NtSetInformation for delete'
            item = syscallName + '(' + filename + ')'
        else:
            syscallName = 'NtSetInformation for rename'
            item = syscallName + '(' + filename + ', ' + newFileName + ')'
    if syscallNumber == 'c':
        syscallName = 'NtClose'
        item = syscallName + '(' + filename + ')'
    return item

def filterProcess(logfilename, fileList, directoryList):
    firstFilteredProcess = {}
    f = open(logfilename, 'r')
    for eachline in f:
        eachline = eachline.strip('\n')
        if eachline.startswith("[") and eachline.endswith("]"):
            eachline = eachline[1 : len(eachline) - 1]
            arrayLine = eachline.split(",")
            filename = arrayLine[3]
            processName = arrayLine[1]
            if processName != '' and filename.lower() in fileList:
                if processName not in firstFilteredProcess:
                    processPath = arrayLine[7]
                    firstFilteredProcess[processName] = {"processPath" : processPath}
    secondFilteredProcess = []
    print firstFilteredProcess
    for eachProcess in firstFilteredProcess:
        if firstFilteredProcess[eachProcess]["processPath"].lower() not in directoryList:
            secondFilteredProcess.append(eachProcess)
    return secondFilteredProcess

def getNewFileIndex(filename, newFileNameList):
    flag = False
    index = 0
    for eachNewFile in newFileNameList:
        if (filename in eachNewFile) or (eachNewFile != '' and eachNewFile in filename):
            flag = True
            break
        index += 1
    if flag:
        return index
    else:
        return -1
    
def analysis(fileList, logfilename, executProcess, resultPath):# fileList here make no sense
    f = open(logfilename, 'r')
    # num = len(fileList)
    num = 20
    print "this is num"
    print num
    sortList = []
    eachFileMemberList = []
    newFileNameList = []
    i=0
    for x in xrange(num):
        sortList.append([])
        eachFileMemberList.append([])
        newFileNameList.append('')
    
    for eachline in f:                                
        eachline = eachline.strip('\n')
        if eachline.startswith("[") and eachline.endswith("]"):
            eachline = eachline[1 : len(eachline) - 1]
            arrayLine = eachline.split(",")
            filename = arrayLine[3]                     
            filename = filename.lower()
            if(filename.startswith('\\??\\c:')):
                filename = filename[6:]
            processName = arrayLine[1]
            newFileName = arrayLine[6]
            syscallNumber = arrayLine[0]
            if processName.lower() == executProcess.lower():
            	if syscallNumber !='4':
            	

                #I dont care if filename is in fileList
	                if filename not in sortList and i<num and '.' in filename:
	                    sortList[i] = filename
	                    i=i+1
	                if filename in sortList :
	                    k = sortList.index(filename)
	                    newFileName = newFileName.lower()
	                    if(newFileName.startswith('\\??\\c:')):
	                        newFileName = newFileName[6:]
	                    eachFileMemberList[k].append(filterMember(arrayLine,filename,newFileName))

    
    f.close()
    for n in xrange(num):
        
        memberList = []
        for item in eachFileMemberList[n]:
            memberList.append('[' + item + ' ,1]')
        statisticsResult = merge(memberList)
        output2(statisticsResult, resultPath)
    


def getAnalysisResults(logfilePath, fileList, directoryList):
    logFileList = getFileListFromDirectory(logfilePath)
    #print logFileList
    for logfilename in logFileList:
        resultPath = '/home/tf/Desktop/result/' + logfilename.split('/').pop()
        executProcessList = filterProcess(logfilename, fileList, directoryList)
        if len(executProcessList) == 1:
            executProcess = executProcessList[0]
            analysis(fileList, logfilename, executProcess, resultPath)
        else:
            filename = resultPath
            f = open(filename, 'a')
            f.write('When deal with ' + logfilename + ' encountered with error：get process error!!!')
            f.write(os.linesep + '~' * 200 + os.linesep)
            f.close()

    for logfilename in logFileList:
        resultPath = '/home/tf/Desktop/netresult/' + logfilename.split('/').pop()
        executProcessList = filterProcess(logfilename, fileList, directoryList)
        if len(executProcessList) == 1:
            executProcess = executProcessList[0]
            NetINfoOutPut(executProcess,logfilename,fileList,resultPath);
 

        else:
            filename = resultPath
            f = open(filename, 'a')
            f.write('When deal with ' + logfilename + ' encountered with error：get process error!!!')
            f.write(os.linesep + '~' * 200 + os.linesep)
            f.close()


def getTimeInfo(executProcess,fileName,fileList,resultPath):
    ransomProcess = executProcess
    TimeList=[]
    f = open(fileName, 'r')
    Min_time = Max_time = 0
    
    # 时间虽然可以直接得到，但是是不能够直接用的
    # 得到第一个被恶意进程攻击的文件出现的时间
    # 2017-8-14 10:29:47:11063
    for eachline in f:
        eachline = eachline.strip('\n')
        if eachline.startswith("[") and eachline.endswith("]"):
            eachline = eachline[1 : len(eachline) - 1]
            arrayLine = eachline.split(",")
            operateTime = arrayLine[-1]
            processName = arrayLine[1]
            syscallName = arrayLine[0]
            if processName ==ransomProcess.lower():
                if syscallName != '4':# notice: we can add controlId to get accurate time
                    if syscallName == '24':
                        print operateTime
                        temp_time = operateTime
                        timeArray = time.strptime(temp_time, "%Y-%m-%d %H:%M:%S:%f")
                        Min_time = time.mktime(timeArray)
                        print syscallName
                        break
    # 得到最后一个被恶意进程攻击的文件出现的时间
    for eachline in f:
        eachline = eachline.strip('\n')
        if eachline.startswith("[") and eachline.endswith("]"):
            eachline = eachline[1 : len(eachline) - 1]
            arrayLine = eachline.split(",")
            
            processName = arrayLine[1]
            operateTime = arrayLine[-1]
            syscallName = arrayLine[0]

            if processName == ransomProcess.lower():
                if syscallName != '4':                     
                # 得到所有文件进程的处理时间信息
                    timeArray = time.strptime(operateTime, "%Y-%m-%d %H:%M:%S:%f")
                    timestamp = time.mktime(timeArray)
                    Max_time = timestamp
                    tempSyscall = syscallName
    print tempSyscall                
    f.close()
    TimeList.append(Min_time)
    TimeList.append(Max_time)
    # print TimeList
    return TimeList


def getMinTime(executProcess,fileName,fileList,resultPath):
    infectedFileList = getTimeInfo(executProcess,fileName,fileList,resultPath)
    T1 = infectedFileList[0]
    return T1

def getMaxTime(executProcess,fileName,fileList,resultPath):
    infectedFileList = getTimeInfo(executProcess,fileName,fileList,resultPath)
    T2 = infectedFileList[1]
    return T2


def NetINfoOutPut(executProcess,fileName,fileList,resultPath):
    f = open(fileName, 'r')
    t1 = getMinTime(executProcess,fileName,fileList,resultPath)
    t2 = getMaxTime(executProcess,fileName,fileList,resultPath)
    firstNetList_1 = []
    firstNetList_2 = []
    firstNetList_3 = []
    print t1
    print t2
    for eachline in f:                                
        eachline = eachline.strip('\n')
        if eachline.startswith("[") and eachline.endswith("]"):
            eachline = eachline[1 : len(eachline) - 1]
            arrayLine = eachline.split(",")
            controlId = arrayLine[3]                     
            newFileName = arrayLine[6]
            syscallName = arrayLine[0]
            processName = arrayLine[1]
            tempTime = arrayLine[-1]
            
            timeArray = time.strptime(tempTime, "%Y-%m-%d %H:%M:%S:%f")
            operateTime = time.mktime(timeArray)
            # print operateTime
            if  processName.lower() == executProcess.lower() or processName.lower() == 'explore.exe' or processName == 'svchost.exe':
                # print operateTime
                if syscallName == '4':

                    if controlId == '0x12003' or controlId == '0x12007':
                        ipAdrr = arrayLine[6]
                        item = syscallName + '(' + controlId + ', ' + ipAdrr + ')'+"----->"
                    if controlId == '0x1201f':
                        bufferLength = arrayLine[6]
                        item = syscallName + '(' + controlId + ', ' + bufferLength + ')'+"----->"
                    if controlId == '0x12017':
                        bufferLength = arrayLine[6]
                        item = syscallName + '(' + controlId + ', ' + bufferLength + ')'+"----->"
                    if controlId == '0x12023':
                        ipAdrr = arrayLine[6]
                        item = syscallName + '(' + controlId + ', ' + ipAdrr + ')'+"----->"
                    if  controlId == '0x1201b':
                        ipAdrr =arrayLine[6]
                        item = syscallName + '(' + controlId + ', ' + ipAdrr + ')'+"----->"
                    else:
                        operate = arrayLine[6]
                        item = syscallName + '(' + controlId + ', ' + operate + ')'+"----->"


                    if operateTime<t1:
                        firstNetList_1.append(item)
                    if operateTime<t2 and operateTime>t1:
                        firstNetList_2.append(item)
                    if operateTime>t2:
                        firstNetList_3.append(item)
        
    f = open(resultPath,'a')
    for item in firstNetList_1:
        str = "A"+item
        f.write(str)
    for item in firstNetList_2:
        str = "B"+item
        f.write(str)

    for item in firstNetList_3:
        str = "C"+item
        f.write(str)
    f.close()

       

fileList = ['\\test\\test\\math.doc', '\\mydocument\\mypdf\\design-pattern-java.pdf','\\test\\ppt_module\\ppt1.pptx', '\\test\\add\\execel_1.xls' ,'\\test\\test\\resume_yuzhi.pdf', '\\test\\test\\story.txt', '\\test\\test\\linux_kernel.zip', '\\test\\test\\voice1.mp3', '\\test\\test\\pic1.jpg', '\\test\\test\\pic1.png', '\\test\\test\\pic1.bmp', '\\test\\test\\theory.mp4']
directoryList = ['c:\\windows\\system32\\', 'c:\\windows\\', 'c:\\users\\win32_init\\desktop\\ss_2.5.8_3.3.2\\shadowsocks-2.5.8\\', '\\\?\\c:\\windows\\system32\\wbem\\']
#processList = ['svchost.exe', 'explorer.exe', 'csrss.exe', 'consent.exe', 'dllhost.exe', 'winlogon.exe', 'searchindexer.exe', 'wmiadap.exe', 'wmiprvse.exe', 'lsass.exe', 'searchprotocolhost.exe', 'taskmgr.exe', 'taskhost.exe']
logfilePath = "/home/tf/Desktop/log/"

getAnalysisResults(logfilePath, fileList, directoryList)

