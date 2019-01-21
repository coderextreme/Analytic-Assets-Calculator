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

# Was macht eigentlich diese schhhhheijnä Dadai ???
# man kann zeit begrenzen oder auch nicht
# man kann csv datei wählen
# man kann das dann speichern oder auch als graph ausgeben
# gemacht werden muss also dass das ne lib wird und ausführung getrennt ist
# gemacht werden muss dazu dass kombis oder kombis von kombis genommen werden
# können für: chartausgabe oder in datei speichern

class csvTimed():
    def __init__(self,filename,distance,types):
        self.navObj = csvMatch.NavigateCSV(filename,0,distance,types)
        self. __SetTimeRanges()

    def __init__(self,filename):
        self.navObj = csvMatch.NavigateCSV(filename,0,300,csvMatch.types.crygold)
        self. __SetTimeRanges()


    def __init__(self):
        self.navObj = csvMatch.NavigateCSV(sys.argv[1],0,300,csvMatch.types.crygold)
        self. __SetTimeRanges()


    def __SetTimeRanges(self):
        self.setFrom()
        self.setUntil()

    def __isOurDateTimeStringThing(self,text):
        blub=re.match('[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}:[0-9]{2}',text)
        if blub == None:
            return False
        else:
            return True
    def __assureOurDateTimeStringThing(self,text):
        if self.__isOurDateTimeStringThing(text):
            return True
        else:
            #print('Falsches DatumZeitFormat')
            #raise AssertionError()
            #exit(1)
            return False

    def __makeTimeStamp(self,text):
        if self.__assureOurDateTimeStringThing(text):
            date_ = datetime.datetime.strptime(text, "%Y-%m-%d_%H:%M")
            return calendar.timegm(date_.utctimetuple())
        else:
            if re.match('[0-9]+',text) != None:
                date_ = int(text)
                return date_
    def setFrom(self,from_):
        self.from_=self.__makeTimeStamp(from_)
    def setUntil(self,until):
        self.to_=self.__makeTimeStamp(until)
    def setFrom(self):
        self.from_=self.__makeTimeStamp(sys.argv[2])
    def setUntil(self):
        if len(sys.argv)>3:
            self.to_=self.__makeTimeStamp(sys.argv[3])
        else:
            self.to_ = time.time() + 1000000000
    def toFile(self,filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for csvline in self.newMatrix:
                writer.writerow(csvline)
            csvfile.close()
        return self
    def chartDisplayForNow(self):
        npMatrix = np.array(self.newMatrix).transpose()
        #data = self.newMatrix  #= np.genfromtxt(sys.argv[1], delimiter=';', skip_header=0, skip_footer=0, names=['x', 'y'])
        dates=[datetime.datetime.fromtimestamp(ts) for ts in npMatrix[0]]
        fig, ax = plt.subplots()
        ax.plot(dates, npMatrix[1], color='r', label='the data')
        plt.show()

    def run(self):
        self.newMatrix = self.navObj.getMatrixBetweenTwoTimestampsOrKeys(self.from_,self.to_)
        return self
    def test(self):
        print(str(self.newMatrix[0])+' '+str(self.newMatrix[-1]))
        return self

blub = csvTimed().run()
#print(str(argv[4]))
if len(sys.argv)>4:
    blub.toFile(sys.argv[4])
else:
    blub.chartDisplayForNow()
#blub=re.match('[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}:[0-9]{2}','2018-02-03_14:05')
#print(str(blub))
#datum=datetime.datetime.strptime('2018-02-03_14:05', "%Y-%m-%d_%H:%M")
## eigentlich werden Timestamps generell in UTC verstanden und verarbeitet
#ts=calendar.timegm(datum.utctimetuple())
#print(str(ts))
##raise AssertionError()
#####print('after')
