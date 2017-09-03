#!/usr/bin/python
# -*- coding: UTF-8 -*-
from os import listdir
from os.path import isfile, join
import os
import Queue
import threading
import time




def getFileName(filePath):
	onlyfiles = [ directory + '/' + f for f in listdir(directory) if isfile(join(directory,f)) ]
    return onlyfiles

//返回恶意进程 return  ransomProcess
def getRansomProcess(fileList,directoryList,fileName):
	firstFilteredProcess = {}
    f = open(fileName, 'r')
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
    RansomProcess = []
    print firstFilteredProcess
    for eachProcess in firstFilteredProcess:
        if firstFilteredProcess[eachProcess]["processPath"].lower() not in directoryList:
            RansomProcess.append(eachProcess)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
    return RansomProcess

   


# 再遍历一次，进程名跟RansomProcess相同，
# 就把该进程操作的文件名保存下来，建立一个数组，
# 记录执行的操作，后面再遇到对该文件的操作，都记录下来。
def getInfectedFilesName(fileList,directoryList,fileName):
	ransomProcess=getRansomProcess(fileList,directoryList,fileName)
	i==0
	infectedFilesList=[]
	f = open(fileName, 'r')
    for eachline in f:
        eachline = eachline.strip('\n')
        if eachline.startswith("[") and eachline.endswith("]"):
            eachline = eachline[1 : len(eachline) - 1]
            arrayLine = eachline.split(",")
            filename = arrayLine[3]
            processName = arrayLine[1]
            operateTime = arrayLine[8]
            if processName == ransomProcess.lower():
            	if filename not in infectedFilesList:						//这里应该怎么确定是遍历的所有i 
            	
            		infectedFilesList[i][0] = fileName
            		infectedFilesList[i][1] = operateTime
            		i++

    return infectedFilesList

def getFirstTime(fileList,directoryList,fileName):
	infectedFileList = getInfectedFilesName(fileList,directoryList,fileName)
	T1 = infectedFilesList[0][1]
	
	return T1

def getLastTime(fileList,directoryList,fileName):
	infectedFileList = getInfectedFilesName(fileList,directoryList,fileName)
	T2 = infectedFilesList[-1][1]

	return T2

def fileInfoOutPut( ):

def netInfoOutput_1( fileList,directoryList,fileName):
	t1 = getFirstTime(filList,directoryList,fileName)
	t2 = getLastTime (fileList,directoryList,fileName)
	f = open(fileName, 'r')
    for eachline in f:
        eachline = eachline.strip('\n')
        if eachline.startswith("[") and eachline.endswith("]"):
            eachline = eachline[1 : len(eachline) - 1]
            arrayLine = eachline.split(",")
            filename = arrayLine[3]
            processName = arrayLine[1]
            operateTime = arrayLine[8]
            if operateTime<t1:
            	pass

            else:
            	break

def netInfoOutput_2( fileList,directoryList,fileName):
	t1 = getFirstTime(filList,directoryList,fileName)
	t2 = getLastTime (fileList,directoryList,fileName)
	f = open(fileName, 'r')
    for eachline in f:
        eachline = eachline.strip('\n')
        if eachline.startswith("[") and eachline.endswith("]"):
            eachline = eachline[1 : len(eachline) - 1]
            arrayLine = eachline.split(",")
            filename = arrayLine[3]
            processName = arrayLine[1]
            operateTime = arrayLine[8]
            if operateTime<t1:
            	pass
            else if t1<operateTime<t2:
            	//operate

            else:
            	break

# 重复遍历的次数太多！！！
def netInfoOutput_3( fileList,directoryList,fileName):
	
	t2 = getLastTime (fileList,directoryList,fileName)
	f = open(fileName, 'r')
    for eachline in f:
        eachline = eachline.strip('\n')
        if eachline.startswith("[") and eachline.endswith("]"):
            eachline = eachline[1 : len(eachline) - 1]
            arrayLine = eachline.split(",")
            filename = arrayLine[3]
            processName = arrayLine[1]
            operateTime = arrayLine[8]
            sys_call = arrayLine[0]
            
            
            	# 把所有系统调用号为0x4的按照顺序进行排序
            	# 排序的标准为控制码
            	# 把结果转化为一个和操作文件时一样的列表形式
            	

            if processName.lower() == executProcess.lower()://当进程名与可疑恶意进程名相同时
            	# if sys_call == '4':
            	# 	# 我们把网络有关的调用也当做是文件，把它放到文件中去，
            	# 	# 显然在现有文件名中是不存在的，所以我们把它们放到新文件当中去
            	# 	i = getNewFileIndex(filename, fileList)
            	# 	if i >= 0:
            	# 		newFileNameList[i] = filename
                #       eachFileMemberList[i].append(filterMember(arrayLine, filename, newFileName))
                if filename in fileList and arrayLine[0] == '149' and newFileName != ''://NtSetInfortmationFile（用于删除文件或者重命名文件）且在排除文件名单内
                    i = fileList.index(filename)//filename在文件列表中的索引
                    newFileName = newFileName.lower()
                    if(newFileName.startswith('\\??\\c:')):
                        newFileName = newFileName[6:]
                    newFileNameList[i] = newFileName//  把新文件名写入新文件名列表，索引值为filename在排除文件列表的索引
                if filename not in fileList and arrayLine[0] == '42' and arrayLine[4] == '0x5'://不在排除名单而且系统调用为42且有标志0x5
                    i = getNewFileIndex(filename, fileList)
                    if i >= 0:
                        newFileNameList[i] = filename
                        eachFileMemberList[i].append(filterMember(arrayLine, filename, newFileName))
                if filename in fileList:
                    i = fileList.index(filename)               //如果文件在排除文件列表中，输出系统调用信息
                    eachFileMemberList[i].append(filterMember(arrayLine, filename, newFileName))//输出系统调用名（文件名）
                elif filename in newFileNameList:
                    i = newFileNameList.index(filename)
                    eachFileMemberList[i].append(filterMember(arrayLine, filename, newFileName))//如果文件名在新文件名列表中，输出系统调用名（文件名，新文件名）
                else:
                    i = getNewFileIndex(filename, newFileNameList)
                    if i >= 0:
                        eachFileMemberList[i].append(filterMember(arrayLine, filename, newFileName))
    f.close()

            
            
           



logfilePath = "C:\\Users\\Administrator\\Desktop\\log\\"

fileList = ['\\test\\test\\math.doc', '\\test\\ppt_module\\ppt1.pptx', '\\test\\add\\execel_1.xls' ,'\\test\\test\\resume_yuzhi.pdf', '\\test\\test\\story.txt', '\\test\\test\\linux_kernel.zip', '\\test\\test\\voice1.mp3', '\\test\\test\\pic1.jpg', '\\test\\test\\pic1.png', '\\test\\test\\pic1.bmp', '\\test\\test\\theory.mp4']
directoryList = ['c:\\windows\\system32\\', 'c:\\windows\\', 'c:\\users\\win32_init\\desktop\\ss_2.5.8_3.3.2\\shadowsocks-2.5.8\\', '\\\?\\c:\\windows\\system32\\wbem\\']
getAnalysisResults(logfilePath, fileList, directoryList)