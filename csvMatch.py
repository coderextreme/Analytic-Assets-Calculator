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
base_path = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(base_path, 'lib'))
import numpy as np
import matplotlib.pyplot as plt
import LibCrygoldEVA
import chartdata2less
import logging
import inspect
#import operations

logger = logging.getLogger('PyCryGold')
logger.setLevel(logging.DEBUG)

import warnings
warnings.filterwarnings("ignore")

# Diese Datei kann:
# CSV Dateien zusammenführen, verrechnend miteinander In neue mündend
# CSV Dateien browsen, d.h. set get Pos Nr und set Pos nahest timestamp +
# getContent dazu
# eingebaut sind operatororientierte (mul,div) Zusammenführungen,
# was zu alt2alt und volumen und damit indizes führen soll

# Das war es eigentlich schon - mehr macht diese Datei gar nicht +fg+
# Oh Gott und für diesen Scheiß habe ich so ewig gebraucht,
# Schande über mein Haupt, erst Teer und dann Federn

# nach vorn springen muss ich noch einprogrammieren, damit der den ganzen Mist
# am Anfang nicht mitlesen muss, wenn der den braucht



class NavigateCSV():
    """ Diese Klasse ist zum finden von Sachen bei gleichen Zeitwerten
        Die Klasse ist nicht zum vollständigen Einlesen von CSV Charts,
        sondern zum Einlesen bis zu einem Timestamp und
                zum Finden ähnlicher verglichener Timestamps zwischen
                    2 CSV Chart Dateien
        Außerdem kann diese Klasse Daten zwischen Timestamps als
        Matrix herausgeben, die algorithmisch gefunden werden damit
          später wäre es noch sinnvoll einzubauen, dass die Klasse
          nicht immer den ganzen Anfang mit einliest.
          Es ist bereits so, dass nur bis zu einem Punkt gelesen wird.
    """


    @property
    def i(self):
        return len(self.haveReadCsv) - 1

    @i.setter
    def i(self,toset):
        raise ValueError('i shall not be set')
        return

    @property
    def pos(self):
        if self.count2 < 1:
            raise ValueError('Count2 shall not be < 1 B')
        if self.i - self.count2 + 1 < 0 or self.i - self.count2 + 1 > len(self.haveReadCsv):
#            logger.debug('index wrong: '+str(self.i)+' '+str(self.count2)+' '+str(len(self.haveReadCsv)))
            if self.i - self.count2 + 1 < 0:
                raise ValueError('Index negative when getting Pos')
            if self.__isIndexOutOfBoundsAbove():
                raise ValueError('Index too high when getting Pos')
            return None
        return self.i - self.count2 + 1

    def __setPosWithoutTakingCare(self,toset):
        self.count2 = self.i - toset + 1 # mehrmals genau durchgerechnet, stimmt
        if self.count2 < 1:
            raise ValueError('Count2 shall not be < 1 A')
#        logger.debug('POS became '+str(self.pos))
        self.pos

    def __isIndexOutOfBoundsAbove(self):
        return self.i - self.count2 + 1 > len(self.haveReadCsv)

    def __toSetIsOutofBoundsAbove(self,toset):
        return toset > len(self.haveReadCsv) - 1

    @pos.setter
    def pos(self,toset):
#        logger.debug('POS was '+str(self.pos))
#        logger.debug('POS shall become '+str(toset))
        if self.i < 0:
            #            raise ValueError('No Data in Matrix')
            if self.__eachCsvLine:
                self.pos = toset
            else:
                self.posSettable = -1
            return
        if toset < 0:
            #raise ValueError('Index negative')
            self.posSettable = -1
            return
        if toset == self.pos:
            if self.i - self.count2 + 1 < 0:
                self.posSettable = -1
            if self.__isIndexOutOfBoundsAbove():
                self.posSettable = 1
            return
        else:
            if toset <= self.i:
                self.posSettable = 0
                self.__setPosWithoutTakingCare(toset)
                return
            else:
                self.count2 = 1
                if self.__toSetIsOutofBoundsAbove(toset):
                    # if index over have had read into
                    if self.hasFileFullRead:
                        self.posSettable = 1
                        return
                    else:
                        while not self.hasFileFullRead and self.__toSetIsOutofBoundsAbove(toset):
                            self.__eachCsvLine()
                        if not self.__toSetIsOutofBoundsAbove(toset):
                            self.posSettable = 0
                            self.__setPosWithoutTakingCare(toset)
                        else:
                            self.posSettable = 1
                            return
        self.posSettable = 0
        self.__setPosWithoutTakingCare(toset)
        return
    @property
    def RowAtPos(self):
        return self.haveReadCsv[self.pos]
    @property
    def TimestampAtPos(self):
        return int(math.floor(float(self.RowAtPos[0])))

    @property
    def PriceAtPos(self):
        return self.RowAtPos[1]


    def __init__(self, filenameOrMatrix,beginTimeStamp,distance):
        self.rek = 0
        #print('is: '+str(filenameOrMatrix))
        #print(str(distance))
        #print(str(len(filenameOrMatrix)))
        try:
            distance = int(distance)
        except:
            distance = 0
        if isinstance(filenameOrMatrix,str):
            self.fromFiles = True
        else:
            if isinstance(filenameOrMatrix,(list,)):
                self.fromFiles = False
        if self.fromFiles:
            #self.i = 0
            self.last=None
            self.count2 = 1
            self.hasFileFullRead = False
        else:
            #self.i = len(filenameOrMatrix)-1
            self.last=filenameOrMatrix[-1]
            self.count2 = 1
            self.hasFileFullRead = True
        self.csvfile = None
        self.csviterator = None
        self.insertLineOfaType = None
        #print(str(distance))
        if distance == 3600:
            #print(str(distance))
            # Weil CSV Zeile noch eine Spalte in der Mitte hat
            self.insertLineOfaType = self.__lineOfVolume
        else:
            self.insertLineOfaType=self.__lineOfChart
        if self.fromFiles:
            self.csvfile=open(filenameOrMatrix, newline='')
            self.csviterator = csv.reader(self.csvfile, delimiter=';', quotechar='|')
            self.haveReadCsv=[]
            self.first=int(float(self.csviterator.__next__()[0]))
        else:
            self.haveReadCsv=filenameOrMatrix
            self.first = self.haveReadCsv[0][0]
        if not str(distance).isnumeric:
            raise "muss numeric sein!"
        self.oneStepSeconds=int(distance)
        self.OneTimeStampCompareAllWith=beginTimeStamp
        if self.fromFiles:
            self.csvfile.close()
            self.csvfile=open(filenameOrMatrix, newline='')
            self.csviterator = csv.reader(self.csvfile, delimiter=';', quotechar='|')
        #self.__forward()

    def __del__(self):
        try:
            if self.csvfile != None:
                self.csvfile.close()
        except :
            pass

    def __insertYes(self,val):
        if len(self.haveReadCsv) == 0:
            return True
        else:
            if self.haveReadCsv[-1][0] == val:
                #print('dbl')
                return False
            else:
                return True

    def __lineOfChart(self):
            val = int(float(self.last[0]))
            if self.__insertYes(val):
                try:
                    self.haveReadCsv.append([val,float(self.last[1])])
                except:
                    pass
    def __lineOfVolume(self):
            val = int(float(self.last[0]))
            if self.__insertYes(val):
                self.haveReadCsv.append([val,float(self.last[2])])
    def __eachCsvLine(self):
        if self.hasFileFullRead:
            return False
        try:
            self.last=self.csviterator.__next__()
            self.insertLineOfaType()
        except StopIteration:
            #alx print('last element')
            self.hasFileFullRead=True
            return False
        #self.i+=1
        return True

#    def __forward(self):
#        if self.hasFileFullRead:
#            return int(self.last[0])
#        if self.fromFiles:
#            wasAtPos=-float("inf")
#            while abs(self - self.OneTimeStampCompareAllWith) < abs(wasAtPos - self.OneTimeStampCompareAllWith) :
#                wasAtPos = self.getWhatAtPos()
#                if not self.__eachCsvLine():
#                    break
#            if not self.hasFileFullRead and self.i>1:
#                self.count2+=1
    def readUntilEndOfFile(self):
        while self.__eachCsvLine():
            pass

    def getAllElementData(self):
        return self.i,self.count2,self.pos,self.TimestampAtPos
    def __CompareWantedWithLocatedTimeStamp1(self):
        return self.OneTimeStampCompareAllWith > self.TimestampAtPos
    def __CompareWantedWithLocatedTimeStamp2(self):
        return self.OneTimeStampCompareAllWith < self.TimestampAtPos

    def __goToWantedTimestamp(self):
        #self.OneTimeStampCompareAllWith
        if self.i == -1:
            if not self.__eachCsvLine():
                raise 'file empty'
        #timestampAtPos = int(math.floor(float(self.TimestampAtPos)))
            #print('a'+str(self.OneTimeStampCompareAllWith ))
            #print('b'+str(self.TimestampAtPos))
        if self.OneTimeStampCompareAllWith == self.TimestampAtPos:
            return
        else:
            if self.OneTimeStampCompareAllWith > self.TimestampAtPos:
               compare = self.__CompareWantedWithLocatedTimeStamp1
               plusminus = 1
            else:
               compare = self.__CompareWantedWithLocatedTimeStamp2
               plusminus = -1
            compare2 = True
            while compare2:
                posbefore = self.pos
                self.pos += plusminus
                compare2 =  self.posSettable == 0 and compare() and self.pos != posbefore
            if posbefore != self.pos and \
            abs(self.TimestampAtPos - self.OneTimeStampCompareAllWith) \
            > abs(math.floor(float(self.haveReadCsv[posbefore][0])) - self.OneTimeStampCompareAllWith):
                    self.pos -= plusminus
            #if self.newPos == posbefore and self.newPos > 1:
            #    logger.debug('too much')
            #    self.setPos(self.newPos-3)

    def getAllAtSimilarTimestampOrKey(self,p):
        self.setToAtSimilarTimestampOrKey(p)
        #print(str(self.getAllElementData()))
        return self.RowAtPos
    def setToAtSimilarTimestampOrKey(self,p):
        self.OneTimeStampCompareAllWith=p
        self.__goToWantedTimestamp()
        return self

    def getMatrixBetweenTwoTimestampsOrKeys(self,begin_,end_):
        from_ = int(self.setToAtSimilarTimestampOrKey(begin_).pos)
        to_ = int(self.setToAtSimilarTimestampOrKey(end_).pos)
#        logger.debug('from to B: '+str(from_)+' '+str(to_))
        if from_ == to_:
            from_ -= 1
        return self.haveReadCsv[from_:to_]
    def toChartObject(self):
        return OperandsContentHandling(self.oneStepSeconds,self.haveReadCsv,"None","None","None")

def isFloatsList(liste_):
    if type(liste_) is list:
        #print(str(type(filename2_OrMatrix2_OrNumber)))
        if len(liste_) > 0:
            if type(liste_[0]) in [float,np.float64]:
                return True
            else:
#                    print(str(type(filename2_OrMatrix2_OrNumber[0])))
                return False
        else:
            return False
    else:
        return False

class OperandTypes(IntEnum):
    @abstractmethod
    def getOperandType(var):
        if type(var) is str:# and isinstance(filename2_OrMatrix2_OrNumber,str):
            return OperandTypes.file_
        elif type(var) in [list,tuple] and len(var) > 0 and not var[0] is list and type(var[0]) in [float,np.float64]:
            return OperandTypes.floatlist
        elif type(var) is list and len(var) > 0 and type(var[0]) is list:
            return OperandTypes.matrix
        elif type(var) in [float,np.float64]:
            return OperandTypes.float_
        else:
            raise ValueError("Operand Type Wrong")
    float_ = 0
    floatlist = 1
    matrix = 2
    file_ = 3


class join2CSVs():
    """ Diese Klasse liest eine Datei vollstaendig ein, ausser Dopplungen
        wegen diesem einen Bug
        diesen Abschnitt in neu zu erschaffende Klasse ausschneiden
        for line1 in self.fileOneTable:
            f2line = self.fileNr2NaviObj.getAllAtSimilarTimestampOrKey(int(line1[0]))
            timestampNew=int((f2line[0]+int(line1[0]))/2)
            #self.append(timestampNew,[[float(line1[1])/f2line[1]],[f2line[1]/float(line1[1])]])
            self._addToNewCVS(timestampNew,self.calcs(line1[1],f2line[1]))

            Außerdem __init_ auf mehrere kleinere methoden vielleicht
    """

    @abstractmethod
    def __init__(self, filename1orMatrix1,filename2_OrMatrix2_OrNumber,type_,stepseconds2,typesHandling):
        operandTypes = []
        operandTypes.append(OperandTypes.getOperandType(filename1orMatrix1))
        operandTypes.append(OperandTypes.getOperandType(filename2_OrMatrix2_OrNumber))
        self.calcs = None
        if operandTypes[0] == OperandTypes.file_:
            self.fn=[filename1orMatrix1.split('/')[-1],filename2_OrMatrix2_OrNumber.split('/')[-1]]
            OneStepSec = LibCrygoldEVA.CommandParameterManaging.getOneStepSeconds(filename1orMatrix1)
        else:
            OneStepSec = 0
        self.calcs = typesHandling.getCalcDelegat()
        self.inall=[]
        self.all=[[self.inall]]
#        if operandTypes[1] in [OperandTypes.file_,OperandTypes.matrix] \
#        and not operandTypes[0] in [OperandTypes.file_,OperandTypes.matrix]:

        if operandTypes[0] in [OperandTypes.file_,OperandTypes.matrix]:
            self.navObj1=NavigateCSV(filename1orMatrix1,0,OneStepSec)
            self.navObj1.readUntilEndOfFile()
        else:
            self.navObj1 = None
        # if both is CSV or first is CSV
        print("abcde "+str(operandTypes[0])+" "+str(operandTypes[1]))
        if operandTypes[0] in [OperandTypes.matrix,OperandTypes.file_] \
        and operandTypes[1] in [OperandTypes.matrix,OperandTypes.file_]:
            self.fileNr2NaviObj = NavigateCSV(filename2_OrMatrix2_OrNumber,0,stepseconds2)
            self.fileNr2NaviObj.setToAtSimilarTimestampOrKey(int(math.floor(float(self.navObj1.haveReadCsv[0][0]))))
            if len(self.fileNr2NaviObj.haveReadCsv) > len(self.navObj1.haveReadCsv) and not operandTypes[1] == OperandTypes.floatlist:
                self.fileNr2NaviObj, self.navObj1 = self.navObj1, self.fileNr2NaviObj
                switch = True
            else:
                switch = False
            if operandTypes[1] == OperandTypes.floatlist:
                for line1 in self.navObj1.haveReadCsv:
                    self._addColumnToNewCVS(line1[0],line1[1:],filename2_OrMatrix2_OrNumber)
            else:
                for line1 in self.navObj1.haveReadCsv:
                    f2line = self.fileNr2NaviObj.getAllAtSimilarTimestampOrKey(math.floor(float(line1[0])))
                    timestampNew=int(math.floor(math.floor(float(f2line[0])+math.floor(float(line1[0])))/2))
                    #self._addToNewCVS(timestampNew,self.calcs(line1[1],f2line[1]))
                    #print('a '+str([f2line[1:],line1[1:]]))
                    if switch:
                        #print("aaa1a "+str(len(line1)))
                        self._addColumnToNewCVS(timestampNew,f2line[1:],line1[1:])
                    else:
                        #print("aaa1b "+str(len(f2line)))
                        self._addColumnToNewCVS(timestampNew,line1[1:],f2line[1:])
        # if first is number
        elif operandTypes[0] == OperandTypes.float_ and operandTypes[1] in [OperandTypes.matrix,OperandTypes.file_]  and not self.calcs is None: # subReverse und divReverse unnötig
            self.fileNr2NaviObj = NavigateCSV(filename2_OrMatrix2_OrNumber,0,stepseconds2)
            for row in self.fileNr2NaviObj.haveReadCsv:
                self._addColumnToNewCVS(row[0],[filename1orMatrix1],row[1:])
        elif operandTypes[1] == OperandTypes.float_ and operandTypes[0] in [OperandTypes.matrix,OperandTypes.file_]  and not self.calcs is None: # subReverse und divReverse unnötig
            self.fileNr2NaviObj = None
            for row in self.navObj1.haveReadCsv:
                self._addColumnToNewCVS(row[0],row[1:],[filename2_OrMatrix2_OrNumber])
        elif operandTypes[0] == OperandTypes.floatlist and operandTypes[1] in [OperandTypes.matrix,OperandTypes.file_,OperandTypes.floatlist] and not self.calcs is None: # subReverse und divReverse unnötig
            #self.fileNr2NaviObj = None
            if not operandTypes[1] == OperandTypes.floatlist:
                self.fileNr2NaviObj = NavigateCSV(filename2_OrMatrix2_OrNumber,0,stepseconds2)
                for row in self.fileNr2NaviObj.haveReadCsv:
                    #print(str(row[1:])+' '+str(filename2_OrMatrix2_OrNumber))
                    self._addColumnToNewCVS(row[0],filename1orMatrix1,row[1:])
            elif self.calcs.__name__ in ['_aswell']:
                self.fileNr2NaviObj = None
                self.all=[[list(filename1orMatrix1+filename2_OrMatrix2_OrNumber)]]
                #print("sdf2 "+str(self.all[0][0][0]))
            else:
                raise ValueError("shall be Operator \"aswell\" or first shall not be a list of floats when second is list of floats")
        elif operandTypes[1] == OperandTypes.floatlist and operandTypes[0] in [OperandTypes.matrix,OperandTypes.file_,OperandTypes.floatlist] and not self.calcs is None: # subReverse und divReverse unnötig
            #print('sdsdf '+str(filename2_OrMatrix2_OrNumber))
            self.fileNr2NaviObj = None
            if not operandTypes[0] == OperandTypes.floatlist:
                for row in self.navObj1.haveReadCsv:
                    #print(str(row[1:])+' '+str(filename2_OrMatrix2_OrNumber))
                    self._addColumnToNewCVS(row[0],row[1:],filename2_OrMatrix2_OrNumber)
            elif self.calcs.__name__ in ['_aswell']:
                self.all=[[list(filename1orMatrix1+filename2_OrMatrix2_OrNumber)]]
                #print("sdf2 "+str(self.all[0][0][0]))
            else:
                raise ValueError("shall be Operator \"aswell\" or first shall not be a list of floats when second is list of floats")
        # if calc with result as just one number instead of whatever else
        # here a quantile
        elif self.calcs is None and type_ == LibCrygoldEVA.calcStackOp.quantileOfAll and operandTypes[1] == OperandTypes.float_:
            self.fileNr2NaviObj = None
            line= []
            transposed = np.array(self.navObj1.haveReadCsv).transpose()
            for column in transposed[1:]:
                line.append(np.quantile(column,filename2_OrMatrix2_OrNumber / 100))
            self.inall.append([self.navObj1.haveReadCsv[0][0]] + line)
            self.inall.append([self.navObj1.haveReadCsv[-1][0]] + line)
        elif OperandTypes.float_ is operandTypes[0] and OperandTypes.float_ is operandTypes[1] and not self.calcs is None:
            print("HERE")
            self.fileNr2NaviObj = None
            if not self.calcs.__name__ in ['_aswell']:
                self.all=[[self.calcs(filename1orMatrix1,filename2_OrMatrix2_OrNumber)]]
            else:
                self.all=[[self.calcs(filename1orMatrix1,filename2_OrMatrix2_OrNumber)]]
        elif OperandTypes.floatlist is operandTypes[0] and OperandTypes.floatlist is operandTypes[1] and OperandTypes.floatlist is operandTypes[1] and not self.calcs is None:
            self.fileNr2NaviObj = None
            result = []
            for a,b in zip(filename1orMatrix1,filename2_OrMatrix2_OrNumber):
                result.append(self.calcs(a,b))
            self.all=[[result]]
        elif OperandTypes.floatlist == operandTypes[0] and OperandTypes.float_ == operandTypes[1] and not self.calcs is None:
            self.fileNr2NaviObj = None
            result = []
            for a in filename1orMatrix1:
                result.append(self.calcs(a,filename2_OrMatrix2_OrNumber))
            self.all=[[result]]
        elif OperandTypes.floatlist == operandTypes[1] and OperandTypes.float_ == operandTypes[0] and not self.calcs is None:
            self.fileNr2NaviObj = None
            result = []
            for b in filename2_OrMatrix2_OrNumber:
                result.append(self.calcs(filename1orMatrix1,b))
            self.all=[[result]]
        else:
            #print(str(self.calcs is join2CSVs._mul))
            raise ValueError("Calculation type does not exist!")

    def __del__(self):
        pass
        try:
            self.navObj1
            del self.fileOneTable
        except:
            pass
        try:
            self.fileNr2NaviObj
            del self.fileNr2NaviObj
        except:
            pass

#    @abstractmethod
#    def _subReverse(self,a,b):
#            a=float(a)
#            b=float(b)
#            return b-a
#    @abstractmethod
#    def _divReverse(self,a,b):
#            a=float(a)
#            b=float(b)
#            #return [b/a,a/b]
#            return b/a
#    @abstractmethod
#    def _powReverse(self,a,b):
#            a=float(a)
#            b=float(b)
#            return math.pow(b,a)
#    @abstractmethod
#    def _rootReverse(a,b):
#            a=float(a)
#            b=float(b)
#            return math.pow(b,1/a)

    @staticmethod
    def _pow(a,b):
            a=float(a)
            b=float(b)
            return math.pow(a,b)
    @staticmethod
    def _root(a,b):
            a=float(a)
            b=float(b)
            return math.pow(a,1/b)
    @staticmethod
    def _sub(a,b):
            a=float(a)
            b=float(b)
            return a-b
    @staticmethod
    def _div(a,b):
            a=float(a)
            b=float(b)
            #return [a/b,b/a]
            return a/b
#    @staticmethod
#    def _logReverse(a,b):
#            #print('mul')
#            return math.log(b,a)
    @staticmethod
    def _log(a,b):
            #print('mul')
            return math.log(a,b)
    @staticmethod
    def _mul(a,b):
            #print('mul')
            return float(a)*float(b)
    @staticmethod
    def _add(a,b):
            #print('add '+str(a)+' '+str(b)+' '+str(float(a)+float(b)))
            return float(a)+float(b)
    @staticmethod
    def _aswell(a,b):
            return a,b
    @abstractmethod
    def _addColumnToNewCVS(self,timestampNew,Operand1Column_2toN,SecondOperands):
        InInAll = []
        self.inall.append(InInAll)
        InInAll.append(math.floor(float(timestampNew)))

        if not self.calcs.__name__ in ['_aswell']:
            if len(Operand1Column_2toN) != len(SecondOperands):
                for EachOperand1 in Operand1Column_2toN:
                    for EachOperand2 in SecondOperands:
                        InInAll.append(self.calcs(EachOperand1,EachOperand2))
            else:
                for EachOperand1,EachOperand2 in zip(Operand1Column_2toN,SecondOperands):
                    InInAll.append(self.calcs(EachOperand1,EachOperand2))
        else:
            for i,EachOperand1 in enumerate(Operand1Column_2toN):
                InInAll.append(EachOperand1)
            for EachOperand2 in SecondOperands:
                InInAll.append(EachOperand2)
            #print("abcde "+str(InInAll))

        # liste in liste hat variable die  bekommt listen appended
        # liste hat variable bekommt je rechnungen liste die bekommt liste per
        # column
        # [][][][]
        # [][][]
#                self._addColumnToNewCVS(row[0],row[1:],filename2_OrMatrix2_OrNumber)
#                    self._addColumnToNewCVS(row[0],self.calcs(column,filename2_OrMatrix2_OrNumber))
#        self.newcsv1.append([timestampNew,a[0]])
#        if len(a) > 1:
#            raise ValueError("calculated result must not be greater than in one dimension")
            #self.newcsv2.append([timestampNew,a[1]])
        #print('jau '+str(self.newcsv1[-1]))

#    @abstractmethod
#    def bothTo_2files(self):
#        raise "depreciated"
#        #print(str(len(self.all[0][1])))
#        for filename,csvtable in self.all:
#            with open(filename, 'w', newline='') as csvfile:
#                writer = csv.writer(csvfile, delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
#                for csvline in csvtable:
#                    writer.writerow(csvline)
#                csvfile.close()
    @abstractmethod
    def get(self):
        return self.all
    def toChartObjects(self):
        obj_=[]
        logger.debug('ppp '+str(self.fileNr2NaviObj))
        if self.fileNr2NaviObj != None:
            OneStepSec = self.fileNr2NaviObj.oneStepSeconds
        else:
            OneStepSec = None
        logger.debug('resultlen: '+str(self.all[0][0]))
        #print(str(isFloatsList(self.all[0][0][0])))
        #print(str((self.all[0][0][0])))
        #if isFloatsList(self.all[0][0][0]):
        #    print("sdf "+str(self.all[0][0][0]))
        #    #obj_.append(self.all[0][0][0])
        #    obj_.append(OperandsContentHandling(OneStepSec,self.all[0][0][0],"None","None","None"))
        #else:
        obj_.append(OperandsContentHandling(OneStepSec,self.all[0][0],"None","None","None"))
            #if len(self.all) == 1:
            #    if len(self.all[0]) == 2:
            #        obj_.append(OperandsContentHandling(OneStepSec,self.all[0][1],"None","None","None"))
        return obj_


#class joinAnyHow(join2CSVs):
#    def __init__(self,chartfilename1,chartfilename2,operation,diffseconds2,new1name="None",new2name="None"):
#        super().__init__(chartfilename1,chartfilename2,operation,diffseconds2,new1name,new2name)
        #super().bothTo_2files()

#class joinChartsByMul(join2CSVs):
#    def __init__(self,chartfilename1,chartfilename2,diffseconds2,new1name="None",new2name="None"):
#        super().__init__(chartfilename1,chartfilename2,LibCrygoldEVA.calcStackOp.mul,diffseconds2,new1name,new2name)
#        #super().bothTo_2files()
#
#class join2Volume(join2CSVs):
#    #die 3600 steht für die zweite Angabe der Multiplikation
#    def __init__(self,chartfilename1,amountOfAllCoins,diffseconds2,new1name="None"):
#        super().__init__(chartfilename1,amountOfAllCoins,LibCrygoldEVA.calcStackOp.mul,diffseconds2,new1name)
#        #super().bothTo_2files()

class AllAlt2Alt:
    def __init__(self):
        dir_ = '/home/alex/workspace-noneclipse/crycsv/coins/'
        for fname1 in os.listdir(dir_):
            for fname2 in os.listdir(dir_):
                if fname1 != fname2:
                    print('ja')
                    #joinCharts(dir_+fname1,dir_+fname2)

#AllAlt2Alt()
##a=joinCharts('GLD-BTC.csv','MYR-BTC.csv')
##del a
##b=join2Volume('LTC-BTC.csv','marketcap/LTC')
##vgl.bothTo_2files()
## hinteres ist distance
#exit(0)
#ncsv = NavigateCSV('test.csv',349,1000)
#ncsv.forward()
##alx print(str(ncsv.getAllElementData()))
#ncsv.__iterateRecursive()
##alx print(str(ncsv.i))
##alx print(str(ncsv.count2))
##alx print(str(len(ncsv.haveReadCsv)))
##alx print(str(ncsv.newPos))
##alx print(str(ncsv.getWhatAtPos()))
##alx print(str(ncsv.getAllElementData()))
##alx print('Ich muss noch machen, dass alle Rechnungen mit div und mal mit ALLEN Zahlen gehen ALLLLEN')
#ncsv.setPos(1)
##alx print(str(ncsv.getAllElementData()))
#ncsv.setPos(5)
##alx print(str(ncsv.getAllElementData()))
#ncsv.setPos(204)
##alx print(str(ncsv.getAllElementData()))
#ncsv.setPos(3)
##alx print(str(ncsv.getAllElementData()))
###alx print(str(ncsv.getAllElementData()))
##ncsv.OneTimeStampCompareAllWith=500
##ncsv.iterateRecursive()
###alx print(str(ncsv.getAllElementData()))
#ncsv.test(901)
#ncsv.test(90)
#ncsv.test(900)
#ncsv.test(210)
#ncsv.test(450)
#ncsv.test(540)
#ncsv.test(700)
#ncsv.test(755)

class OperandsContentHandling():

    class __OperandsContentType(IntEnum):
        matrix = 0
        matrices = 1
        floats = 2
        listOfFloats = 3
        filename = 4
        nothing = 5
        primitive = 6

    class __Subclasses2use(IntEnum):
        matrixMatricesFilename = 0
        listOfFloats = 1
        unknown = 2
        primitive = 3

    @staticmethod
    def _isFloat(primitive):
        if type(primitive) in [float,np.float64]:
            return True
        try:
            primitive = float(primitive)
            if type(primitive) in [float]:
                return True
        except:
            return False
        return False


    @staticmethod
    def _isFloatsList(liste_):
        if type(liste_) in [tuple,list]:
            print('type '+str(type(liste_[0])))
            if len(liste_) > 0:
                if type(liste_[0]) in [float,np.float64]:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    @staticmethod
    def _isOneValuePerTimestamp(matrix):
        if type(matrix) is list:
            if type(matrix) is list or type(matrix) is np.ndarray \
            and len(matrix) > 0:
                if len(matrix[0]) == 2 and len(matrix[-1]) == 2 \
                and type(matrix[0]) is list and type(matrix[-1]) is list \
                and not type(matrix[0][0]) is list and not type(matrix[-1][-1]) is list:
                    return True
        return False

    @staticmethod
    def _isMultiValuesPerTimestamp(matrix):
        if type(matrix) is list:
            if type(matrix) is list or type(matrix) is np.ndarray \
            and len(matrix) > 0:
                if len(matrix[0]) > 2 and len(matrix[-1]) > 2 \
                and type(matrix[0]) is list and type(matrix[-1]) is list \
                and not type(matrix[0][0]) is list and not type(matrix[-1][-1]) is list:
                    return True
        return False

    @staticmethod
    def _isFilename(filename):
        if type(filename) is str:
            return os.path.isfile(filename)
        return False

    def __init__(self,oneStepSeconds,operandsContent,name,what,inwhat):
        if self._isFilename(operandsContent):
            self.__contentType = self.__OperandsContentType.filename
        elif self._isFloat(operandsContent):
            self.__contentType = self.__OperandsContentType.primitive
        elif self._isFloatsList(operandsContent):
            self.__contentType = self.__OperandsContentType.listOfFloats
        elif self._isOneValuePerTimestamp(operandsContent):
            self.__contentType = self.__OperandsContentType.matrix
            self.matrices = None
            self.matrix = operandsContent
        elif self._isMultiValuesPerTimestamp(operandsContent):
            self.__contentType = self.__OperandsContentType.matrices
            self.matrices = operandsContent
            self.matrix = None
        else:
            self.__contentType = self.__OperandsContentType.nothing
        if self.__contentType in [self.__OperandsContentType.filename,self.__OperandsContentType.matrix,self.__OperandsContentType.matrices]:
            self.whichSubclass =  self.__Subclasses2use.matrixMatricesFilename
            self.__class__ = ChartdataHandling
            self.__init__(oneStepSeconds,operandsContent,name,what,inwhat)
        elif self.__contentType is self.__OperandsContentType.primitive:
            self.whichSubclass =  self.__Subclasses2use.primitive
            self.__class__ = PrimitiveOperandDataContentHandling
            self.__init__(oneStepSeconds,operandsContent,name,what,inwhat)
        elif self.__contentType is self.__OperandsContentType.listOfFloats:
            self.whichSubclass =  self.__Subclasses2use.listOfFloats
            self.__class__ = ListOperandDataContentHandling
            self.__init__(oneStepSeconds,operandsContent,name,what,inwhat)
        else:
            self.whichSubclass =  self.__Subclasses2use.unknown
            print("contentType: "+str(self.__contentType))
            raise AssertionError("Not Supported Operand Type, and though unknown Type")

    @abstractmethod
    def toCsvFile(self,filenameAndPath):
        pass
    @abstractmethod
    def toPyStdStructure(self):
        pass
    @abstractmethod
    def toPrintCSV(self):
        pass
    @abstractmethod
    def toDiseplayChart(self):
        pass
    @abstractmethod
    def toReturnCSV(lf):
        pass
    @abstractmethod
    def toCsvFile(self,filenameAndPath):
        pass

class PrimitiveOperandDataContentHandling(OperandsContentHandling):

    def __init__(self,oneStepSeconds,primitive,name,what,inwhat):
        self.primitive = primitive

    def toPyStdStructure(self):
        return self.primitive

    def toPrintCSV(self):
        print(str(self.primitive))

    def toDisplayChart(self):
        print("Result is just a one dimensional List, that is not capable to be output as Chart Diagram.")

class ListOperandDataContentHandling(OperandsContentHandling):

    def __init__(self,oneStepSeconds,listOfFloats,name,what,inwhat):
        self.listOfFloats = listOfFloats

    def toPyStdStructure(self):
        return self.listOfFloats

    def toPrintCSV(self):
        for val in self.listOfFloats:
            print(str(val))
    def toDisplayChart(self):
        print("Result is just a one dimensional List, that is not capable to be output as Chart Diagram.")


class ChartdataHandling(OperandsContentHandling):
    def __init__(self,oneStepSeconds,filenameOrMatrix,name,what,inwhat):
        logger.debug('filenameOrMatrixLen: '+str(len(filenameOrMatrix)))
        self.OneStepSeconds=oneStepSeconds # 300 or 900 or 3600
        self.name=name
        self.what=what
        self.inwhalt=inwhat
        self.matrices = None
        if type(filenameOrMatrix) is str:
            navCSV=NavigateCSV(filenameOrMatrix,0,self.OneStepSeconds) # hier muss types anders
            #navCSV.forward()
            navCSV.readUntilEndOfFile()
            self.matrix=navCSV.haveReadCsv
        else:
            if type(filenameOrMatrix) is list or type(filenameOrMatrix) is np.ndarray \
            and len(filenameOrMatrix) > 0:
                if len(filenameOrMatrix[0]) == 2 and len(filenameOrMatrix[-1]) == 2 \
                and type(filenameOrMatrix[0]) is list and type(filenameOrMatrix[-1]) is list \
                and not type(filenameOrMatrix[0][0]) is list and not type(filenameOrMatrix[-1][-1]) is list:
                #and len(filenameOrMatrix[0][0]) == 1 and len(filenameOrMatrix[-1][-1]) == 1: :
                    self.matrix=filenameOrMatrix
                else:
                    #print(str(len(filenameOrMatrix))+' '+str(len(filenameOrMatrix[0])))
                    #if len(filenameOrMatrix) == 4 \
                    #and len(filenameOrMatrix[0]) > 0 and len(filenameOrMatrix[-1]) > 0  \
                    #and len(filenameOrMatrix[0][0]) == 2 and len(filenameOrMatrix[-1][-1]) == 2:
                    if len(filenameOrMatrix) > 0:
                        if len(filenameOrMatrix[0]) > 1:
                            self.matrices = filenameOrMatrix
                            self.matrix = None
                        else:
                            raise ValueError("wrong len")
                    else:
                        raise ValueError("wrong len")
            else:
                if type(filenameOrMatrix) is ChartdataHandling:
                    #print("aaa1")
                    self.matrix = ChartdataHandling.toPyStdStructure
                else:
                    #print(str(type(filenameOrMatrix)))
                    raise "neither Matrix input, nor File"
    def getOneStepSeconds(self):
        return self.OneStepSeconds
    def toCsvFile(self,filenameAndPath):
        with open(filenameAndPath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for csvline in self.matrix:
                writer.writerow(csvline)
            csvfile.close()
        return self
    def toPyStdStructure(self):
        if self.matrix == [] or not self.matrix is None:
            return self.matrix
        elif self.matrices == [] or not self.matrices is None:
            return self.matrices
    def toReturnCSV(self):
        a = ''
        if self.matrix != None:
            for line in self.matrix:
                for el in line:
                    a+=str(el)
                    if not el is line[-1]:
                        a+=';'
                a+='\n'
        else:
            try:
                if self.matrices != None:
                    yes_ = True
                else:
                    yes_ = False
            except ValueError:
                yes_ = True
            if yes_:
                #for matrix in np.transpose(self.matrices,(1,0)):
                for matrix in self.matrices:
                    for line in matrix:
                        for i,el in enumerate(line):
                            a+=str(el)
                            #if i == 0:
                        a+=';'
                        #print('|', end='')
                    a+='\n'
        return a
    def toPrintCSV(self):
            #print('x')
            #print(str(resulttoken.token.toPyStdStructure()))
            #print('x')
        if self.matrix == [] or self.matrix != None:
            for line in self.matrix:
                for el in line:
                    print(str(el), end='')
                    if not el is line[-1]:
                        print(';', end='')
                print('')
        else:
            if self.matrices == [] or not self.matrices is None:
                #for matrix in np.transpose(self.matrices,(1,0)):
                for matrix in self.matrices:
                    for line in matrix:
                        print(str(line)+';', end='')
                        #for i,el in enumerate(line):
                        #    print(str(el), end='')
                        #    #if i == 0:
                        #print(';', end='')
                        ##print('|', end='')
                    print('')
    def toDisplayChart(self):
        if self.matrix != None:
            npMatrix = np.array(self.matrix).transpose()
            dates=[datetime.datetime.fromtimestamp(float(ts)) for ts in npMatrix[0]]
            fig, ax = plt.subplots()
            ax.plot(dates, npMatrix[1], color='r', label='the data')
        else:
            if self.matrices == [] or not self.matrices is None:
                mat =  []
                for i,m in enumerate(self.matrices):
                    mat.append([])
                    for k,el in enumerate(m):
                        mat[-1].append(float(el))
                npMatrix = np.array(mat).transpose()
                #for lines in mat:
                #    print(str(lines[0]))
                #print(str(npMatrix))
                dates = [datetime.datetime.fromtimestamp(float(ts)) for ts in npMatrix[0]]
                #print(str(dates))
                fig, ax = plt.subplots()
                #colors = ['k','b','r','y']
                #things = ['Average','Min','Max','Median']
                for k,column in enumerate(npMatrix):
                    #for i,el in enumerate(self.matrices[k]):
                    #    if i != 0:
                    #        #print(str(el))
                    #        #self.matrices[k][i]=float(el)
                    #        pass
                    if k != 0:
                        #ax.plot(dates[1:], npMatrix[k][1:], color=colors[k-1], label=things[k-1])
                        ax.plot(dates, npMatrix[k])
                plt.title("Med Max Avg Med")
                plt.legend()
        plt.show()


#chartdata2less.ReduceDataToFourThings(OperandsContentHandling(300,'/home/alex/workspace-noneclipse/crycsv/coins/BTCD-BTC.csv','','','')).test()
#chartdata2less.ReduceDataToFourThings('/home/alex/workspace-noneclipse/crycsv/coins/BTCD-BTC.csv').test()
