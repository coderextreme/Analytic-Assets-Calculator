#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import re
import sys
import subprocess
import time
import datetime
import csv
from enum import IntEnum
import statistics
import math
from abc import ABCMeta, abstractmethod
import os
import calendar
import re
import csvMatch
import numpy as np
import matplotlib.pyplot as plt
import os.path
import Stack
from operations import OpTypesHandling as opTypesThings
from operations import calcStackOp
import CursorNToken
import logging
import StackTree

logger = logging.getLogger('PyCryGold')
logger.setLevel(logging.DEBUG)

# Was macht eigentlich diese schhhhheijnä Dadai ???
# man kann zeit begrenzen oder auch nicht
# man kann csv datei wählen
# man kann das dann speichern oder auch als graph ausgeben
# gemacht werden muss dazu dass kombis oder kombis von kombis genommen werden
# können für: chartausgabe oder in datei speichern


class ParameterTypes(IntEnum):
    @staticmethod
    def isOurDateTimeStringThing(text): # kein self wohl weil enum klasse
        blub=re.match('d?[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}:[0-9]{2}',text)
        if blub == None:
            return False
        else:
            return True
    Date = 1
    FileExistingOrReservedWord = 2
    NonExistingInFolder = 3
    operationWithTwoOperands = 4
    NoneElse = 5
    number = 6
    FlattenType = 7
    BracketOpen = 8
    BracketClose = 9
    operationWithOneOperand = 10
    operationWithThreeOperands = 11



class CommandParameterManaging():
    """
    Es muss vom Typ der Argumente sein input1.csv int [mul input2.csv int |div input2.csv] [2000-01-01_01:01 [2020-01-01_01:01]] [outfile.csv]
    """

    @staticmethod
    def getOneStepSeconds(filenameAndPath):
        if type(filenameAndPath) is str and not re.match(r"^[-+]?\d*\.\d+|\d+$",filenameAndPath) and not CommandParameterManaging.__isBracketOpen(filenameAndPath) and not CommandParameterManaging.__isBracketClose(filenameAndPath):
            filename = filenameAndPath.split('/')[-1]
            if re.match('^[A-Z0-9]+$',filename):
                a = 3600
            elif re.match('^bitfinex\-[a-z0-9]+\.csv$',filename):
                a = 1800
            elif re.match('^[a-zA-Z0-9]+\-[a-zA-Z0-9]+\.csv$',filename):
                a = 300
            elif re.match('^gewicht.*csv$',filename):
                a = 7200
            else:
                logger.debug("File Type Error, Filename: "+str(filename))
                raise ValueError("File Type Error " + filenameAndPath)
        else:
            a = 300
        logger.debug('Set OneStepSeconds: '+str(a))
        return a

    @staticmethod
    def isFlattenType(text):
        if type(text) is str and len(text) > 1 and text[-1] in ['d','w','m','h'] and str(text[:1]).isnumeric():
            return True
        else:
            return False
    @staticmethod
    def __isOperationWithOneOperand(text):
        if opTypesThings.isAnOperation(text):
            return calcStackOp.amountOperands(opTypesThings.EnumKeyByStrKey(text)) == 1
        else:
            return False
    @staticmethod
    def __isOperationWithTwoOperands(text):
        if opTypesThings.isAnOperation(text):
            return calcStackOp.amountOperands(opTypesThings.EnumKeyByStrKey(text)) == 2
        else:
            return False
    @staticmethod
    def __isOperationWithThreeOperands(text):
        if opTypesThings.isAnOperation(text):
            return calcStackOp.amountOperands(opTypesThings.EnumKeyByStrKey(text)) == 3
        else:
            return False

    def __isFileExistingOrReservedWord(self,text):
        isFileExisting = os.path.isfile(text)
        if isFileExisting and len(self.isTypes) != 0:
            self.__OneStepSeconds.append(self.getOneStepSeconds(text))
        return isFileExisting \
        or text == 'chart' or text == 'graph' or text == 'variable' \
        or text == 'stdout' or text == 'None' or text == 'none'
    @staticmethod
    def __isBracketOpen(text):
        if len(text) > 0:
            return ( text[0]=="(" ) or ( text[0]=="[") or ( text[0]=="{" )
        else:
            return False
    @staticmethod
    def __isBracketClose(text):
        if len(text) > 0:
            return ( text[-1]==")" ) or ( text[-1]=="]" ) or ( text[-1]=="}" )
        else:
            return False
    @staticmethod
    def __isDate(text):
        return ParameterTypes.isOurDateTimeStringThing(text)
    @staticmethod
    def __isNonExistingInFolder(text):
        if not os.path.isfile(text):
            return os.path.isdir('/'.join(str(text).split('/')[:-1]))
        else:
            return False
#    def __isNonExistingInFolder(self,text):
#        if not os.path.isfile(text):
#            return os.path.isdir('/'.join(str(text).split('/')[:-1]))
#        else:
#            return False

    def __init__(self,array):
        self.__OneStepSeconds = []
        logger.debug("init CommandParameterManaging")
        self.outdata = "init CommandParameterManaging"
        array = self.__toMakeArray(array)
        self.__knowArgvTypes(array).exec()

    @property
    def outdata(self):
        logger.debug("get outdata")
        return self.__outdata

    @outdata.setter
    def outdata(self, outd_):
        logger.debug("set outdata: "+str(outd_))
        self.__outdata = outd_
#    def is_float(self,input):
#        try:
#            num = float(input)
#        except ValueError:
#            return False
#        return True
    def __toMakeArray(self,array):
        if len(array) > 0:
            if ' ' in array[1] and len(array) == 2:
                return [ array[0] ] + array[1].split()
            if len(array) == 3:
                if ' ' in array[1] and not ' ' in array[2]:
                    return [ array[0] ] + array[1].split() + [ array[2] ]
        return array

    def __knowArgvTypes(self,array):
        self.parameterList=array
        self.isTypes=[]
        self.TypesListed=[]
        for el in array:
            if self.__isFileExistingOrReservedWord(el):
                self.isTypes.append(ParameterTypes.FileExistingOrReservedWord)
            elif self.isFlattenType(el):
                self.isTypes.append(ParameterTypes.FlattenType)
            elif self.__isOperationWithOneOperand(el):
                self.isTypes.append(ParameterTypes.operationWithOneOperand)
            elif self.__isOperationWithTwoOperands(el):
                self.isTypes.append(ParameterTypes.operationWithTwoOperands)
            elif self.__isOperationWithThreeOperands(el):
                self.isTypes.append(ParameterTypes.operationWithThreeOperands)
            elif self.__isDate(el):
                self.isTypes.append(ParameterTypes.Date)
            elif self.__isNonExistingInFolder(el):
                self.isTypes.append(ParameterTypes.NonExistingInFolder)
            elif re.match(r"^[-+]?\d*\.\d+|\d+$",el):
                self.isTypes.append(ParameterTypes.number)
            elif self.__isBracketOpen(el):
                self.isTypes.append(ParameterTypes.BracketOpen)
            elif self.__isBracketClose(el):
                self.isTypes.append(ParameterTypes.BracketClose)


            if len(self.isTypes) == 1:
                self.TypesListed.append(self.isTypes[0])
            else:
                if len(self.isTypes) == 0:
                    self.TypesListed.append(ParameterTypes.NoneElse)
                else:
                    raise AssertionError()
            self.isTypes=[]
        return self

#    def getParameterTypes(self):
#        return self.TypesListed
    def __parse(self):
        logger.debug('first: '+str(self.TypesListed[-1]))
        logger.debug('HaveFoundOneStepSeconds: '+str(self.__OneStepSeconds))
        self.outdata += "<br>\nParsing began"
        if len(self.TypesListed) > 0:
            self.outdata += "<br>\nParameters had been set"
            if self.TypesListed[-1] == ParameterTypes.FileExistingOrReservedWord or self.TypesListed[-1] == ParameterTypes.NoneElse:
                self.deltaFromBackwards = 1
                self.outdata += "<br>\n deltaFromBackwards = "+str(self.deltaFromBackwards)
            else:
                #self.deltaFromBackwards = 0
                self.calcStack = []
                self.outdata += "<br>\nLast parameter is neither file nor reserved word nor something else"
                return False,[],[],[]
            if len(self.TypesListed) > 1:
                if self.TypesListed[ -1 - self.deltaFromBackwards] == ParameterTypes.Date:
                    self.dates = 1
                    if len(self.TypesListed) > 2:
                        if self.TypesListed[ -2 - self.deltaFromBackwards] == ParameterTypes.Date:
                            self.dates = 2
                            self.outdata += "<br>\n self.dates = "+str(self.dates)
                else:
                    self.dates = 0
                    self.outdata += "<br>\n self.dates = "+str(self.dates)
            else:
                self.dates = 0
                self.outdata += "<br>\n self.dates = "+str(self.dates)
        else:
            self.outdata += "<br>\nNo parameters at all"
            return False,[],[],[]
        self.outdata += "<br>\nParsing Step B, TypesListed: "+str(self.TypesListed)
        ##printstr(self.dates)+' '+str(deltaFromBackwards))
        if int(self.deltaFromBackwards) + int(self.dates) != 0:
            self.restTypes = self.TypesListed[1: - int(self.deltaFromBackwards) - int(self.dates)]
        else:
            self.restTypes = self.TypesListed[1:]
        self.outdata += "<br>\nParsing Step B, delta: "+str(self.deltaFromBackwards)+" "+str(self.dates)
        self.outdata += "<br>\nParsing Step B, restTypes: "+str(self.restTypes)
        ##printstr(self.restTypes))
        ##printstr(self.TypesListed))
        self.stacktree=StackTree.StackTree(self)
        result = self.stacktree._parseAll(self.restTypes,self.parameterList,None,[True,[],[],None])
        #try:
        #   result[3][0].append(result)
        #except:
        #    raise ""
        #printself.outdata)
        return result
    def exec(self):
        self.wasParsOK=self.__parse()
        if self.wasParsOK[0]:
            #print"bla: "+str(self.stacktree.tree1))
            if self.dates == 1:
                date1=self.parameterList[-1-self.deltaFromBackwards]
                date2=None
            else:
                if self.dates == 2:
                    date1=self.parameterList[-2-self.deltaFromBackwards]
                    date2=self.parameterList[-1-self.deltaFromBackwards]
                else:
                    date1 = None
                    date2 = None
            self.outdata += "<br>\nDates: "+str(date1)+" "+str(date2)
            #self.stacktree._execBracket(self.wasParsOK[1],self.parameterList,self.wasParsOK[2],self.stacktree.tree1)
            self.outdata += "<br>\nCalculation yes 3!"
            mulCharts = ManyCalculations(self.wasParsOK[0],date1,date2,self.wasParsOK[3])
            mulCharts.RestPartCalcListIntoStack().exec()
            self._out(mulCharts)
            combiCalcDone = True
            logger.debug("Calculations had been done 1!")
        else:
            self.outdata += "<br>\nParsing went wrong, No Execution!"
            x=[]
            for y in self.TypesListed:
                x.append(str(y))
            self.ParsingTypesList=x#[[]]
            print(self.outdata)
            print('Es muss vom Typ der Argumente sein input1.csv diffsec1 [mul input2.csv|div input2.csv diffsec2] [2000-01-01_01:01 [2020-01-01_01:01]] NEWoutfile.csv /  \'stdout\' / \'chart\' ')

    def _out(self,ChartLimitedObj):
        #print(str(type(ChartLimitedObj)))
        chartObj = ChartLimitedObj.toChartObject()
        if self.deltaFromBackwards == 0:
            chartObj.toDisplayChart()
        elif self.deltaFromBackwards == 1:
            if self.parameterList[-1] == 'stdout':
                if type(chartObj) is list:
                    for notA_Chart in chartObj:
                        print(str(notA_Chart))
                else:
                    chartObj.toPrintCSV()
            elif self.parameterList[-1] == 'chart' or self.parameterList[-1] == 'graph':
                chartObj.toDisplayChart()
            elif self.parameterList[-1] == 'none' or self.parameterList[-1] == 'None':
                pass
            elif self.parameterList[-1] == 'variable':
                if self.wasParsOK:
                    self.outdata = chartObj
                else:
                    self.outdata += '<br>\n'+str(self.ParsingTypesList)
            else:
                chartObj.toCsvFile(self.parameterList[-1])
#
#    def __parse(self):
#        return self.__doParameterTypeFit()



class ChartDataTimeLimitedPlusTwoOutputs():
    def __init__(self,filename,diffseconds,from_,to_):
        logger.debug('Konstruktor LimitedChart 1: '+str(diffseconds)+' '+str(filename))
        self.navObj = csvMatch.NavigateCSV(filename,0,diffseconds)
        #self.navObj.forward()
        logger.debug('Konstruktor LimitedChart 2: '+str(self.navObj.i)+' '+str(self.navObj.count2)+' '+str(len(self.navObj.haveReadCsv)))
        self.setFrom(from_)
        self.setUntil(to_)
        self.diffseconds=diffseconds
#        self.__SetTimeRanges()

#    def __init__(self,filename):
#        self.navObj = csvMatch.NavigateCSV(filename,0,300,csvMatch.types.crygold)
#        self. __SetTimeRanges()

    #def __init__(self):
     #   self.navObj = csvMatch.NavigateCSV(sys.argv[1],0,300,csvMatch.types.crygold)
     #   self. __SetTimeRanges()


#    def __SetTimeRanges(self):
#        self.setFrom()
#        self.setUntil()

    def __assureOurDateTimeStringThing(self,text):
        #text=str(int(float(text)))
        ##printstr(text))
        if text is None:
            return True
        if  ParameterTypes.isOurDateTimeStringThing(text):
            return True
        else:
            ##print'Falsches DatumZeitFormat')
            #raise AssertionError()
            #exit(1)
            return False

    def __makeTimeStamp(self,text):
        if self.__assureOurDateTimeStringThing(text):
            if text[0] != 'd':
                date_ = datetime.datetime.strptime(text, "%Y-%m-%d_%H:%M")
                return calendar.timegm(date_.utctimetuple())
            else:
                numbers = re.findall(r"[0-9]+",text)
                numbers2 = []
                for number in numbers:
                    numbers2.append(int(number))
                ##printstr(numbers2))
                date_ = int(time.time())-int((((numbers2[0]*12+numbers2[1])*(365.25/12)+numbers2[2])*24+numbers2[3])*60+numbers2[4]+15)*60
                ##printstr(int(time.time()))+'  '+str(int((((numbers2[0]*12+numbers2[1])*int(365.25/12)+numbers2[2])*24+numbers2[3])*60+numbers2[4])*60))
                return date_

        else:
            if re.match('[0-9]+',text) != None:
                date_ = int(text)
                return date_
    def setFrom(self,from_):
        if not from_ is None:
            self.from_=self.__makeTimeStamp(from_)
        else:
            self.from_=int(time.time() - (3600 * 24 * 365 * 10))
        logger.debug('set From: '+str(self.from_))

    def setUntil(self,until):
        if not until is None:
            self.to_=self.__makeTimeStamp(until)
        else:
            self.to_ = int(time.time() + (3600 * 24))
        logger.debug('set Until '+str(self.to_))
#    def toFile(self,filename):
#        with open(filename, 'w', newline='') as csvfile:
#            writer = csv.writer(csvfile, delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
#            for csvline in self.newMatrix:
#                writer.writerow(csvline)
#            csvfile.close()
#        return self
#    def chartDisplayForNow(self):
    def toChartObject(self):
        return csvMatch.OperandsContentHandling(self.diffseconds,self.newMatrix,"None","None","None")
#    def toStdOut(self):
#        for line in self.newMatrix:
#            for el in line:
#                #printstr(el), end='')
#                if not el is line[-1]:
#                    #print';', end='')
#            #print'')
#    def showChart(self):
#        npMatrix = np.array(self.newMatrix).transpose()
#        #data = self.newMatrix  #= np.genfromtxt(sys.argv[1], delimiter=';', skip_header=0, skip_footer=0, names=['x', 'y'])
#        dates=[datetime.datetime.fromtimestamp(ts) for ts in npMatrix[0]]
#        fig, ax = plt.subplots()
#        ax.plot(dates, npMatrix[1], color='r', label='the data')
#        plt.show()

    def run(self):
        logger.debug('run Limited Chart '+str(self.from_)+' '+str(self.to_))
        self.newMatrix = self.navObj.getMatrixBetweenTwoTimestampsOrKeys(self.from_,self.to_)
        ##print'bli '+str(len(self.newMatrix)))
        return self
    def test(self):
        #printstr(self.newMatrix[0])+' '+str(self.newMatrix[-1]))
        return self

class ManyCalculations():
    def __init__(self,calcList,from1,to1,tree1):
        #print"calc tree1: "+str(tree1[2]))
        #print"calc Children: "+str(len(tree1[1])))
        #print"calc Stack: "+str(tree1[2][2]))
        self.calcList = tree1[2][2]
        self.from_ = from1
        self.to_ = to1
        self.Stack_ = Stack.Stack()
        self.tree1 = tree1
        #self.treedepth = 0
        self.treewidth = len(tree1[1]) - 1
        return

    def treework(self):
        if self.treewidth < 0:
            raise ValueError("treewidth error")
        mulCharts = ManyCalculations(None,self.from_,self.to_,self.tree1[1][self.treewidth])
        self.treewidth -= 1
        restPart = mulCharts.RestPartCalcListIntoStack()
        if restPart is None:
            raise ValueError("Restpart shall not be None!")
        else:
            calcresult = restPart.exec().toChartObject()
            if type(calcresult) is float or type(calcresult) is list:
                return calcresult
            else:
                return calcresult.toPyStdStructure()


#    tokentypes = ("()",ParameterTypes.FileExistingOrReservedWord,)

    def dispatchToken(self, token,tokenList,i,tokenShallBeList,counter,wasNumber):
        elementBecome = None
        if True: #token in tokenShallBeList:
            isInt = False
            if token == "()":
                counter += 1
                treeworkresult = self.treework()
                if type(treeworkresult) is str or ( type(treeworkresult) is list and len(treeworkresult) > 0 and type(treeworkresult[0]) is list):
                    elementBecome = ChartDataTimeLimitedPlusTwoOutputs(treeworkresult,0,self.from_,self.to_).run().toChartObject()
                else:
                    elementBecome = treeworkresult
            elif os.path.isfile(token) and wasNumber:
                counter += 1
                elementBecome = ChartDataTimeLimitedPlusTwoOutputs(token,tokenList[i-1],self.from_,self.to_).run()
            elif CommandParameterManaging.isFlattenType(token):
                elementBecome = token
                counter += 1
            elif token in opTypesThings.OpFromEnum.keys() and type(token) is calcStackOp:
                counter -= calcStackOp.amountOperands(token) - 1
                elementBecome = token
            elif (type(token) is str and re.match(r"^[-+]?\d*\.\d+|\d+$",token)):
                elementBecome = float(token)
                counter += 1
            elif type(token) is list:
                elementBecome = []
                for tok in token:
                    elementBecome.append(float(tok))
                counter += 1
            elif type(token) is int:
                isInt = True
            else:
                success = False
            success = True
        return success, counter, elementBecome, isInt

    def RestPartCalcListIntoStack(self):
        calcListRev = self.calcList[::-1]
        print(str(self.tree1[2][0]))
        counter = 0
        self.operands = []
        self.operation = None
        wasNumber = False
        for i,token in enumerate(calcListRev):
            counterbefore = counter
            result,counter,newelement, wasNumber = self.dispatchToken(token,calcListRev,i,[],counter, wasNumber)
            if not result:
                #print(str(token)+' at '+str(i)+' in '+str(calcListRev))
                raise ValueError("not any of tokens")
            if counterbefore < counter:
                #print("opnd")
                self.operands.append(newelement)
            elif counterbefore > counter or (type(token) is calcStackOp and calcStackOp.amountOperands(token) == 1):
                #print("op "+str(newelement)+' '+str(calcListRev))
                self.operation = newelement
            elif wasNumber:# or (type(token) is calcStackOp and calcStackOp.amountOperands(token) == 1):
                pass
                #if token in [calcStackOp.negative,calcStackOp.same]:
                #    #self.operands.append(float(-1))
                #    self.operation = newelement
            else:
                raise ValueError("no increment nor decrement")
            if counter == 0:
                print("step: "+str(i)+" "+str(calcListRev[i])+" "+str(len(calcListRev)))
            if counterbefore != counter and \
            ((counter == 0 and i < len(calcListRev) - 2 and i != 0) or (counter == 1 and i + 1 == len(calcListRev))):
                print(str("xxx"))
                print("OPNDS: "+str(len(self.operands)))
                self.__pushing(counter-1)
                self.operands = []
                self.operation = None
                wasNumber = False
        if counter == 1:
            return self
        else:
            return None


#    def RestPartCalcListIntoStack(self):
#        #print"treewidth1: "+str(self.treewidth))
#        tree_property_ParaTypes=self.tree1[2][0]
#        #print"calc 3: "+str(tree_property_ParaTypes))
#        if len(tree_property_ParaTypes) == 1 and tree_property_ParaTypes[0] == ParameterTypes.FileExistingOrReservedWord:
#            #print"calc 4: "+str(tree_property_ParaTypes))
#            onlyOneFileName_InProperties = self.tree1[2][1][1]
#            self.C = ChartDataTimeLimitedPlusTwoOutputs(onlyOneFileName_InProperties,0,self.from_,self.to_).run().toChartObject()
#            #print"calc C: "+str(type(self.C)))
#            return self
#        elif len(self.calcList) == 2 and self.calcList[0] == "()":
#            self.C = ChartDataTimeLimitedPlusTwoOutputs(self.treework(),0,self.from_,self.to_).run().toChartObject()
#            #print"calc C2: "+str(type(self.C)))
#            return self
#        else:
#            self.C = None
#        ##print"calc List: "+str(len(self.calcList))+' '+str(self.calcList))
#        #if (len(self.calcList) -5) % 3 != 0:
#        #    #print"RestPart is become None 1 "+str(len(self.calcList)))
#        #    return None
#        jumpforward = 0
#        calcListRev = self.calcList[::-1]
#        #logger.debug('calcList: '+str(self.calcList[2])+'|'+str(self.calcList[5]))
#        for i,el in enumerate(calcListRev):
#            if jumpforward > 0:
#                jumpforward -= 1
#                continue
#            logger.debug('uuu '+str(i)+' '+str(len(calcListRev)))
#            if len(calcListRev) > i + 1:
#                if calcListRev[i] in opTypesThings.OpFromEnum.keys() and type(calcListRev[i]) is calcStackOp and calcStackOp.amountOperands(calcListRev[i]) == 1:
#                    self.A = None
#                    self.op = calcListRev[i]
#                    deltax = 2
#                    jumpforward -= 2
#                else:
#                    deltax = 0
#                    if not (type(calcListRev[i+1]) is str and re.match(r"^[-+]?\d*\.\d+|\d+$",calcListRev[i+1])):
#                        #print"treewidth1a: "+str(self.treewidth))
#                        if CommandParameterManaging.isFlattenType(calcListRev[i+1]):
#                            self.A = str(calcListRev[i+1])
#                        elif calcListRev[i+1] == '()':
#                            a_result = self.treework()
#                            if type(a_result) is float or type(a_result) is list:
#                                self.A = a_result
#                            elif type(a_result) is list:
#                                if type(a_result[0]) is float:
#                                    self.A = a_result
#                                else:
#                                    raise ValueError("list is not of floats")
#                            else:
#                                self.A = ChartDataTimeLimitedPlusTwoOutputs(a_result,0,self.from_,self.to_).run()
#                            #print"treewidth1b: "+str(self.treewidth)+' '+str(i))
#                        else:
#                            self.A = ChartDataTimeLimitedPlusTwoOutputs(calcListRev[i+1],el,self.from_,self.to_).run()
#                    else:
#                        self.A = float(calcListRev[i+1])
#            else:
#                self.A = None
#            if i >= len(calcListRev) - 5 + deltax and i + 4 - deltax < len(calcListRev):
#                #print"dej "+str(calcListRev)+' '+str(i))
#                #print"calc calcListRev "+str(calcListRev))
#                if calcListRev[i+4-deltax] == '()':
#                    #print"dej2a "+str(calcListRev))
#                    #print"treewidth2: "+str(self.treewidth))
#                    self.B = ChartDataTimeLimitedPlusTwoOutputs(self.treework(),0,self.from_,self.to_).run()
#                else:
#                    #print"dej2b "+str(calcListRev))
#                    self.B = ChartDataTimeLimitedPlusTwoOutputs(calcListRev[i+4-deltax],calcListRev[i+3-deltax],self.from_,self.to_).run()
#                jumpforward += 2
#            else:
#                print("No B at "+str(i)+' about '+str(len(calcListRev)))
#                self.B = None
#            #logger.debug('op for Push: '+str(i)+': '+str(calcListRev[i+2]))
#            #print(str(self.A))
#            if not self.A is None:
#                self.op = calcListRev[i+2]
#            jumpforward += 2
#            self.__pushing()
#        if jumpforward == 0:
#            return self
#        else:
#            print("RestPart is become None "+str(jumpforward))
#            return None
    def __pushing(self,operandAmountLess):
        if self.operation is None:
            if len(self.operands) != 1:
                raise ValueError("No Operation only allows to have one operand with no operation")
            #else:
            #    self.operands[0] = self.operands[0].toChartObject()
            #return
        else:
            self.Stack_.push(CursorNToken.Token(opTypesThings(self.operation).execOpMethod()))
            if calcStackOp.amountOperands(self.operation) != len(self.operands) - operandAmountLess:
                print(str(self.operands)+" "+str(operandAmountLess))
                raise ValueError("Operations requested amount of operands is not real amount of operands")
        for operand in self.operands:
            if type(operand) is ChartDataTimeLimitedPlusTwoOutputs:
                self.Stack_.push(CursorNToken.Token(operand.toChartObject()))
            elif (not operand is None and str(operand).isnumeric) \
            or   (issubclass(type(operand) ,csvMatch.OperandsContentHandling)):
                self.Stack_.push(CursorNToken.Token(operand))
            else:
                raise ValueError("not supported types of Operands, when pushing into stack")
            print("Operand Pushed: "+str(self.Stack_.top().token))

#    def __pushing(self):
#        if not self.C is None:
#            return
#        self.Stack_.push(CursorNToken.Token(opTypesThings(self.op).execOpMethod()))
#        #logger.debug('op Push A : '+str(self.Stack_.top().token))
#        #logger.debug('op Push A1: '+str(self.Stack_.top().token.LenOperands()))
#        #logger.debug('op Push A2: '+str(type(self.A)))
#
#        #logger.debug('op Push B: '+str(operations.OpAdd()))
#        if type(self.A) is ChartDataTimeLimitedPlusTwoOutputs:
#            self.Stack_.push(CursorNToken.Token(self.A.toChartObject()))
#            #logger.debug('op Push A3: '+str(type(self.A.toChartObject())))
#        elif not self.A is None and str(self.A).isnumeric:
#            self.Stack_.push(CursorNToken.Token(self.A))
#            #logger.debug('op Push A3: '+str(type(self.A)))
#        elif issubclass(type(self.A) ,csvMatch.OperandsContentHandling):
#            self.Stack_.push(CursorNToken.Token(self.A))
#            #logger.debug('op Push A3: '+str(type(self.A)))
#        elif calcStackOp.amountOperands(self.op) == 1:
#            pass
#        else:
#            print(str(type(self.A)))
#            raise ValueError("A ist weder ChartLimited Obj noch Float")
#        logger.debug('op Push A4: '+str(type(CursorNToken.Token(self.A)._token)))
#
#
#        if not self.B is None:
#            self.Stack_.push(CursorNToken.Token(self.B.toChartObject()))
#            logger.debug('op Push C : '+str(self.Stack_.top().token))

    def exec(self):
        #if self.operation is None and len(self.operands) == 1:
        #    self.OperandsContentHandling = self.operands[0]
        #    return self
        while not self.Stack_.isEmpty():
            logger.debug('Multiclass top: '+str(self.Stack_.top))
            #logger.debug('Multiclass top: '+str(self.Stack_._stack[-2]))
            resulttoken = self.Stack_.pop()
            try:
                logger.debug('result in Multiclass: '+str(len(resulttoken.token.toPyStdStructure())))
            except:
                pass
        if resulttoken.isOperandsContentHandling:
            self.OperandsContentHandling = resulttoken.token
        print(str(type(resulttoken._token)))
        return self

    def toChartObject(self):
        return  self.OperandsContentHandling
