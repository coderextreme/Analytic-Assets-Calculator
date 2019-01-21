#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import csv
import numpy
import matplotlib.pyplot as plt
import datetime
import LibCrygoldEVA

lines=[]
matrix=[]
for line1 in sys.stdin:
    line2 = str(line1).split(';')
    line3 = []
    for el in line2:
        try:
            line3.append(float(el))
        except:
            print(str(el))
    matrix.append(line3)


def showChart(matrix):
    chartObj = LibCrygoldEVA.csvMatch.ChartdataHandling(0,matrix,"",None,None)
    chartObj.toDisplayChart()
#    npMatrix = numpy.array(matrix).transpose()
#    dates=[datetime.datetime.fromtimestamp(ts) for ts in npMatrix[0]]
#    fig, ax = plt.subplots()
#    ax.plot(dates, npMatrix[1], color='r', label='the data')
#    plt.show()

showChart(matrix)
