#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import csv
import numpy
import matplotlib.pyplot as plt
import datetime
import subprocess

def alxexec(command):
        stdoutdata = subprocess.getoutput(command)
        if len(stdoutdata)!=0:
                print(stdoutdata)
        return stdoutdata

execu=str('ssh alex@diener2 \'/opt/scripts/crycsv/server.py '+' '.join(sys.argv[1:])+'\'')
#execu=str('./server.py '+' '.join(sys.argv[1:]))
#print(execu)
#alxexec(execu)
alxexec(execu+' | '+'/'.join(sys.argv[0].split('/')[:-1])+'/recieve2out.py')
