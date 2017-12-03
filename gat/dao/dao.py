import random

caseDict = {}


def getFileDict(case_num):
    global caseDict
    return caseDict[int(case_num)]


def updateFileDict(case_num, key, value):
    global caseDict
    caseDict[int(case_num)][key] = value


def createFileDict(case_num):
    global caseDict
    if int(case_num) not in caseDict:
        caseDict[int(case_num)] = {}

def setFileDict(fileDict, case_num):
    global caseDict
    caseDict[int(case_num)] = fileDict

def makeCaseNum():
    case_num = 100000 + random.randint(0, 100000)
    createFileDict(case_num)
    return case_num