#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#import math
import requests
import json
#import urllib2
import time
import datetime

r = requests.get('https://www.cryptocompare.com/api/data/coinlist/')
content=r.json()
for key,value in content['Data'].items():
    #print(value['Symbol'])
    g = requests.get('https://www.cryptocompare.com/api/data/CoinSnapshotFullById/?id='+value['Id']).json()
    #print(g['Data']['General']['TotalCoinsMined'])
    amount=g['Data']['General']['TotalCoinsMined']
    if isinstance(amount, float):
        with open("/media/rest/data/marketcap/"+value['Symbol'], "a") as myfile:
            myfile.write(str(time.time())+';'+str(datetime.datetime.now())+";"+str(amount)+";\n")
