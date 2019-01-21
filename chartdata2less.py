#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import subprocess
import time
import datetime
import csv
from enum import IntEnum
import statistics
import math
import numpy as np

class ReduceDataToFourThings():

    class TIMES(IntEnum):
        HOUR = 2
        MDAY = 3
        MONTH = 4

    class calcOps(IntEnum):
        MIN=0
        MAX=1
        AVERAGE=2
        MEDIAN=3
        BEGIN=4
        END=5
        VARIANCE=6
        STANDARDDEVIATION=7
        QUANTILE=8

    def giveTimeSpace(self,cell,times):
        timestring=datetime.datetime.fromtimestamp(int(float(cell))).strftime('%Y %m %d %H %M %S')
        timestring=timestring.split(' ')
        #timestring2=timestring[0]+'-'+timestring[1]+'-'+timestring[2]+'_'+timestring[3]+':'+timestring[4]
        timestring=timestring[0:-times]
        return timestring#,timestring2

    def calcMedAvgMinMax(self,arrays,operation):
        result = []
        arrays = np.transpose(arrays,(1,0))
#        print('sdrf '+str(len(arrays)))
        for array in arrays:
            result.append(self.__calcMedAvgMinMax(array,operation))
        return result

    def __calcMedAvgMinMax(self,array,operation):
        if operation==self.calcOps.AVERAGE:
            return sum(array)/float(len(array))
        if operation==self.calcOps.MIN:
            return min(array)
        if operation==self.calcOps.MAX:
            return max(array)
        if operation==self.calcOps.MEDIAN:
            return statistics.median(array)
        if operation==self.calcOps.BEGIN:
            return array[0]
        if operation==self.calcOps.END:
            return array[-1]
        if operation in [self.calcOps.VARIANCE,self.calcOps.STANDARDDEVIATION]:
            return statistics.variance(array)

#    allOperations=[calcOps.AVERAGE,calcOps.MIN,calcOps.MAX,calcOps.MEDIAN]

    def collectAllMedAvgMinMaxEvery(self,timespandatalist3,timespandatalist,allOperations,times):
        timespandatalist2 = timespandatalist3 + timespandatalist
        range_ = []
        outData2 = []
        numberdifferentDates=len(timespandatalist3)
        #print(str(len(timespandatalist3))+' '+str(len(timespandatalist)))
        if True:
            #from1 = len(timespandatalist3) - 1 - math.floor(numberdifferentDates/2)
            #to1 = len(timespandatalist3) - 1 + math.floor(numberdifferentDates/2)
            #if from1 >= 0 and len(timespandatalist2)<=to1:
            #    from_ = from1
            #    to_ = to1 - 1
            #    print("a")
            #else:
            #    from2 = len(timespandatalist2) - 1 - numberdifferentDates
            #    print("c "+str(from2) )
            #    if from2 >= 0:
            #        from_ = from2
            #        to_ = len(timespandatalist2) - 1
            #        print("b "+ str(to_))
            #    else:
            #        raise ValueError("alx 876")
            #if from_>to_:
            #    raise ValueError("alx 654")
            from_ =  len(timespandatalist2) - 1 - ( 2 * math.floor(numberdifferentDates/2))
            if from_ < 0:
                numberdifferentDates = math.floor(len(timespandatalist2) / 2)
                from_ =  len(timespandatalist2) - 1 - ( 2 * math.floor(numberdifferentDates/2))
                if from_ < 0:
                    raise ValueError("alx 284")
            if math.floor(numberdifferentDates/2)!=0:
                #for k in range(from_,len(timespandatalist2) - 1):
                if True:
                    #begin = k - math.floor(numberdifferentDates/2)
                    #end_ = k + math.floor(numberdifferentDates/2)
                    begin = from_
                    end_ = from_ + numberdifferentDates
                    if end_ >= len(timespandatalist2):
                        end_ = len(timespandatalist2) - 1
                        #raise ValueError("bla")
                    outData1=[]
                    for i,operation in enumerate(self.allOperations):
                        if len(timespandatalist2[begin:end_]) > 0:
                            if i == 0:
                                outData1.append((times))
                            for el in self.calcMedAvgMinMax(timespandatalist2[begin:end_],operation):
                                if operation == self.calcOps.STANDARDDEVIATION:
                                    outData1.append(math.sqrt(el))
                                else:
                                    outData1.append(el)
                    outData2.append(outData1)

            timespandatalist2=[]
        return outData2

    def collectAllMedAvgMinMax(self,timespandatalist2,allOperations,timedata,timedatabefore,times):
        outData1=[]
        #print(str(len(timespandatalist2)))
        if timespandatalist2!=[]:
            for i,operation in enumerate(self.allOperations):
                #print(str(timedata)+' '+str(timedatabefore)+' '+str(self.calcMedAvgMinMax(timespandatalist2,operation))+' '+str(len(timespandatalist2))+' '+str(datetime.datetime.fromtimestamp(int(times)).strftime('%Y %m %d %H %M %S')))
                if i == 0:
                    outData1.append((times))
                for el in self.calcMedAvgMinMax(timespandatalist2,operation):
                    if operation == self.calcOps.STANDARDDEVIATION:
                        outData1.append(math.sqrt(el))
                    else:
                        outData1.append(el)

            timespandatalist2=[]
        return outData1

    def out(self):
        """
            Erster Index Ist Zeile, zweiter ist welches der 4 es ist, dritter is A Timestamp und B Wert
        """
        return self.allOutDatas

    def getDateTypeForMakeLess(self,flattenTypeString):
        if not type(flattenTypeString) is str and len(flattenTypeString) < 2:
            if type(flattenTypeString) is str and str(flattenTypeString).isnumeric:
                return [self.TIMES.MDAY,int(flattenTypeString)]
            raise ValueError
        else:
            mul = int(flattenTypeString[:1])
            dtypes = { 'd' : [self.TIMES.MDAY,mul], \
                       'w' : [self.TIMES.MDAY,7*mul], \
                       'h' : [self.TIMES.HOUR,mul], \
                       'm' : [self.TIMES.MONTH,mul], \
                       'y' : [self.TIMES.MONTH,12*mul] }
            TwoThings = dtypes[flattenTypeString[-1]]
#            TwoThings =  TwoThings[0] , int(TwoThings[1]) * int(flattenTypeString[:1]
#            #print(str(TwoThings)+' '+str(flattenTypeString[-1]))
            return TwoThings


    def __init__(self,chartObj,flattenTypeString,every=False,allOperations=[calcOps.AVERAGE,calcOps.MIN,calcOps.MAX,calcOps.MEDIAN],once=False,quantile=0.5):
        self.allOperations = allOperations
        flattenTypeString = self.getDateTypeForMakeLess(flattenTypeString)
        numberdifferentDates=flattenTypeString[1]
        numberdifferentDatesCountdown=numberdifferentDates
        timedata=''
        timespandatalist=[]
        timespandatalist2=[]
        times2=[]
        self.allOutDatas = []
        timespandatalist3 = []
        for k,row in enumerate(chartObj.toPyStdStructure()):
            times=[]
            for i,cell in enumerate(row):
                if i==0:
                    timedatabefore=timedata
                    timedata=self.giveTimeSpace(cell,flattenTypeString[0])
                    times.append([int(float(cell))])
                    #print("a "+str(timedata) + " a "+str(timedatabefore)+" "+str(numberdifferentDates)+" "+str(numberdifferentDatesCountdown))
                    #timedata2=timedata[1]
                    #timedata=timedata[0]
                if i==1:
                    #print(str(flattenTypeString)+' '+str(flattenTypeString[1])+' '+str(numberdifferentDatesCountdown))
                    if timedata!=timedatabefore and k!=0 and numberdifferentDatesCountdown>0:
                        numberdifferentDatesCountdown-=1
                    cells=[]
                    for cellOf2toN in row[1:]:
                        cells.append(float(cellOf2toN))
                    #print("xxxi "+str(len(cells)))
                    timespandatalist.append(cells)
                    if numberdifferentDatesCountdown == 0:
                        timespandatalist3=timespandatalist
                        timespandatalist2=timespandatalist
                        timespandatalist=[]
                        numberdifferentDatesCountdown=numberdifferentDates
                        #print('x '+str(numberdifferentDates))
                    else:
                        timespandatalist2=[]
            times.append(self.calcMedAvgMinMax(times,self.calcOps.AVERAGE)[0])
            if not every:
                # line only be created when enough data collected
                line = self.collectAllMedAvgMinMax(timespandatalist2, self.allOperations, timedata, timedatabefore,times[-1])
                if line != []:
                    if k == 0:
                        self.allOutDatas.append(self.collectAllMedAvgMinMax(timespandatalist2, self.allOperations, timedata, timedatabefore,chartObj.toPyStdStructure()[0][0]))
                    self.allOutDatas.append(line)
            else:
                lines = self.collectAllMedAvgMinMaxEvery(timespandatalist3, timespandatalist, self.allOperations, times[-1])
                if lines != []:
                    if lines[0] != []:
                        if k == 0:
                            self.allOutDatas.append(self.collectAllMedAvgMinMax(timespandatalist2, self.allOperations, timedata, timedatabefore,chartObj.toPyStdStructure()[0][0]))
                        for line in lines:
                            self.allOutDatas.append(line)
                            #self.allOutDatas.append(self.collectAllMedAvgMinMax(timespandatalist2, self.allOperations, timedata, timedatabefore,times[-1]))
            if once and len(self.allOutDatas) > 0:
                break
        #print(str(lines))
        #print(str(self.allOutDatas[-1]))
        if not every:
            timespandatalist2=timespandatalist
            if len(self.allOutDatas) == 0:
                self.allOutDatas.append(self.collectAllMedAvgMinMax(timespandatalist2, self.allOperations, timedata, timedatabefore,chartObj.toPyStdStructure()[0][0]))
            self.allOutDatas.append(self.collectAllMedAvgMinMax(timespandatalist2, self.allOperations, timedata, timedatabefore,times[-1]))
        else:
            if len(self.allOutDatas) == 0:
                    lines = self.collectAllMedAvgMinMaxEvery(timespandatalist3, timespandatalist, self.allOperations, chartObj.toPyStdStructure()[0][0])
                    for line in lines:
                        self.allOutDatas.append(line)
            lines = self.collectAllMedAvgMinMaxEvery(timespandatalist3, timespandatalist, self.allOperations, times[-1])
            for line in lines:
                self.allOutDatas.append(line)
            if len(self.allOutDatas) == 0:
                timespandatalist2=timespandatalist
                if len(self.allOutDatas) == 0:
                    self.allOutDatas.append(self.collectAllMedAvgMinMax(timespandatalist2, self.allOperations, timedata, timedatabefore,chartObj.toPyStdStructure()[0][0]))
                self.allOutDatas.append(self.collectAllMedAvgMinMax(timespandatalist2, self.allOperations, timedata, timedatabefore,times[-1]))
        if once and len(self.allOutDatas) > 0:
            self.allOutDatas = self.allOutDatas[0][1:]
            #print(str(self.allOutDatas))
        if allOperations == [self.calcOps.END] and len(self.allOutDatas) > 0:
            self.allOutDatas = self.allOutDatas[-1][1:]
            #print(str(self.allOutDatas))
        #for times in self.allOutDatas:
        #    print(str(times[0]))

    def test(self):
        pass
