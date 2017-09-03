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


def output2(statisticsResult, filePath, resultPath):
    #filename = resultPath + '\\' + filePath.split('\\').pop() + '.log'
    f = open(resultPath, 'a')
    count = len(statisticsResult)
    if count == 0:
        f.write(filePath + ' Not Found!!!' + os.linesep)
    else:
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

# //得到ransomware进行第一次文件操作的时间T1和最后一次操作的时间T2
# //def get2Time(arrayLine,filename,newFileName):



def filterMember(arrayLine, filename, newFileName):
    
    syscallNumber = arrayLine[0]
    item = ''
    if syscallNumber == '4':

        syscallName = 'NtDeviceIoControl'
        
        if controlId == 0x12003 or controlId == 0x12007:
            ipAdrr = arrayLine[6]
            item = syscallName + '(' + filename + ', ' + ipAdrr + ')'
        if controlId == 0x1201f:
            bufferLength = arrayLine[6]
            item = syscallName + '(' + filename + ', ' + bufferLength + ')'
        if controlId == 0x12017:
            bufferLength = arrayLine[6]
            item = syscallName + '(' + filename + ', ' + bufferLength + ')'
        if controlId == 0x12023:
            ipAdrr = arrayLine[6]
            item = syscallName + '(' + filename + ', ' + ipAdrr + ')'
        if  controlId == 0x1201b:
            ipAdrr =arrayLine[6]
            item = syscallName + '(' + filename + ', ' + ipAdrr + ')'
        else:
            operate = arrayLine[6]
            item = syscallName + '(' + filename + ', ' + operate + ')'


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
    

def analysis(fileList, logfilename, executProcess, resultPath):
    f = open(logfilename, 'r')
    num = len(fileList)
    eachFileMemberList = []
    newFileNameList = []
    for x in xrange(num):
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
            operateTime = arrayLine[8]
            
            if processName.lower() == executProcess.lower():
                if filename not in fileList and sys_call == '4':
                  # 我们把网络有关的调用也当做是文件，把它放到文件中去，
                  # 显然在现有文件名中是不存在的，所以我们把它们放到新文件当中去
                  # //这里加上对时间的考虑，如果是小于t1,就
                  i = getNewFileIndex(filename, fileList)
                  if i >= 0:
                      newFileNameList[i] = filename
                      eachFileMemberList[i].append(filterMember(arrayLine, filename, newFileName))
                if filename in fileList and arrayLine[0] == '24' and newFileName != '':
                    i = fileList.index(filename)
                    newFileName = newFileName.lower()
                    if(newFileName.startswith('\\??\\c:')):
                        newFileName = newFileName[6:]
                    newFileNameList[i] = newFileName
                if filename not in fileList and arrayLine[0] == '52' and arrayLine[4] == '0x5':
                    i = getNewFileIndex(filename, fileList)
                    if i >= 0:
                        newFileNameList[i] = filename
                        eachFileMemberList[i].append(filterMember(arrayLine, filename, newFileName))
                if filename in fileList:
                    i = fileList.index(filename)              
                    eachFileMemberList[i].append(filterMember(arrayLine, filename, newFileName))
                elif filename in newFileNameList:
                    i = newFileNameList.index(filename)
                    eachFileMemberList[i].append(filterMember(arrayLine, filename, newFileName))
                else:
                    i = getNewFileIndex(filename, newFileNameList)
                    if i >= 0:
                        eachFileMemberList[i].append(filterMember(arrayLine, filename, newFileName))
    f.close()
    for n in xrange(num):
        memberList = []
        for item in eachFileMemberList[n]:
            memberList.append('[' + item + ' ,1]')
        statisticsResult = merge(memberList)
        output2(statisticsResult, fileList[n], resultPath)

def getAnalysisResults(logfilePath, fileList, directoryList):
    logFileList = getFileListFromDirectory(logfilePath)
    #print logFileList
    for logfilename in logFileList:
        # resultPath = '/home/sjp/Desktop/result/' + logfilename.split('/').pop()
        resultPath = 'C:\\Users\\Administrator\\Desktop\\test\\' + logfilename.split('/').pop()
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



fileList = ['\\test\\test\\math.doc', '\\test\\ppt_module\\ppt1.pptx', '\\test\\add\\execel_1.xls' ,'\\test\\test\\resume_yuzhi.pdf', '\\test\\test\\story.txt', '\\test\\test\\linux_kernel.zip', '\\test\\test\\voice1.mp3', '\\test\\test\\pic1.jpg', '\\test\\test\\pic1.png', '\\test\\test\\pic1.bmp', '\\test\\test\\theory.mp4']
directoryList = ['c:\\windows\\system32\\', 'c:\\windows\\', 'c:\\users\\win32_init\\desktop\\ss_2.5.8_3.3.2\\shadowsocks-2.5.8\\', '\\\?\\c:\\windows\\system32\\wbem\\']
#processList = ['svchost.exe', 'explorer.exe', 'csrss.exe', 'consent.exe', 'dllhost.exe', 'winlogon.exe', 'searchindexer.exe', 'wmiadap.exe', 'wmiprvse.exe', 'lsass.exe', 'searchprotocolhost.exe', 'taskmgr.exe', 'taskhost.exe']
logfilePath = "C:\\Users\\Administrator\\Desktop\\log\\"

getAnalysisResults(logfilePath, fileList, directoryList)

#p = threading.Thread(target = updateFileQueue, args = ())
#c = threading.Thread(target = getAnalysisResults1, args = (logfilePath, fileList, directoryList,))

#p.start()
#c.start()
