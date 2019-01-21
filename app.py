#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
#import cgi
#import cgitb
#import web
#cgitb.enable(display=0, logdir="/opt/scripts/crycsv/cgi.log")
# import libraries in lib directory
#import matplotlib
#import numpy
base_path = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(base_path, 'lib'))
#sys.path.insert(0, '/usr/lib/python3.5/site-packages')
#print(str(sys.path))

from flask import Flask
import flask
import collections
import CryGold4Web
#import html5lib
import urllib
app = Flask(__name__)
from os import listdir
from os.path import isfile, join
import json
import traceback
#data = 'A'

#get_response = requests.get(url='http://google.com')
#post_data = {'username':'joeb', 'password':'foobar'}
# POST some form-encoded data:
#post_response = requests.post(url='http://httpbin.org/post', data=post_data)


#form = web.input()

#form = cgi.FieldStorage()

def is_safe_path(basedir, path, follow_symlinks=True):
      # resolves symbolic links
    if follow_symlinks:
        return os.path.realpath(path).startswith(basedir)
    return os.path.abspath(path).startswith(basedir)

def toCSV(cg4w):
    return cg4w.toReturnCSV()

def dirs(mypath):
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles




@app.route('/old')
def beginold():
    website = "<html><head></head><body><form action=\"/runold\"> \
            <input id=\"0\" name=\"0\" value=\"pricecoins/XMG-BTC.csv\"> File <!-- , but that first file not the amountcoin Files --> <br> \
            <input id=\"1\" name=\"1\" value=\"300\"> must be 300 for pricecoin/XXX-XXX.csv , 900 for pricecoin/bitfinex-XXXXXX.csv and 3600 for amountcoins/*.csv <br> \
            <input id=\"2\" name=\"2\" value=\"mul\">  mul or add or div or log or diffuse <br> \
            <input id=\"3\" name=\"3\" value=\"pricecoins/btc-eur.csv\"> File when before mul add div, number if log, \"1d\" if diffuse<br> \
            <input id=\"4\" name=\"4\" value=\"300\"> same with 300 and 3600 as above <br>\
            <input id=\"5\" name=\"5\" value=\"\">  mul or add or div or log or diffuse <br> \
            <input id=\"6\" name=\"6\" value=\"\"> Files when before mul add div, number if log, \"1d\" if diffuse<br> \
            <input id=\"7\" name=\"7\" value=\"\"> same with 300 and 3600 as above <br>\
            <input id=\"8\" name=\"8\" value=\"2018-01-01_00:00\"> DateTimeFormat or with the letter \"d\" before and next line blank a timespan same format<br> \
            <input id=\"9\" name=\"9\" value=\"2018-04-01_00:00\"> DateTimeFormat or Nothing when letter \"d\" is added in front of befors line<br> \
            <button type=\"submit\"> \
            give-Table</button></form><br> \
            <a href=\"/pricecoins.json\">files in pricecoins</a><br><a href=\"/amountcoins.json\">files in amountcoins</a><br> \
            <a href=\"/operations.json\">operations</a><br> \
            </body></html>"
    return website

@app.route('/runold')
def homeold():
    #if "name" not in form or "addr" not in form:
        #a="<H1>Error</H1>"
        #b="Please fill in the name and addr fields."
        #c=str(form)
    #d=form.username
    #    return a+b+d
    #a="<p>name:"+ form["name"].value
    #b="<p>addr:"+ form["addr"].value
    b = []
    for c,a in flask.request.args.items():
        b.append(str(c))
        #b.insert(1,c)
    u = collections.OrderedDict(sorted(flask.request.args.items()))
    d = b[::-1]
    h = ''
    #out_ = CryGold4Web.outdata
    #toCSV(out_)
    #return str(out_.toPyStdStructure().getCmdParaManageObj('/opt/scripts/crycsv/CryGold4Web '+h))
    nono0 = False
    nono = False
    nono2 = False
    for i,(w,o) in enumerate(u.items()):
        if i > 1 and i < 5:
            if str(o) == "":
                nono0 = True
        if i > 4 and i < 8:
            if str(o) == "":
                nono = True
        if i == 9:
            if str(o) == "":
                nono2 = True
    for i,(w,o) in enumerate(u.items()):
        if nono0 and i > 1 and i < 8:
            continue
        if nono and i > 4 and i < 8:
            continue
        if nono2 and i == 9:
            continue
        if i == 0 or i == 3 or i == 6:
            if not is_safe_path('/opt/scripts/crycsv/pricecoins', str(o)) and not is_safe_path('/opt/scripts/crycsv/amountcoins',str(o)):
                return 'File wrong'
        if i != 7 and i != 4 and i != 1:
            h += str(o)+' '
    outObj = CryGold4Web.getCmdParaManageObj('/opt/scripts/crycsv/CryGold4Web '+h)
    if issubclass(type(outObj.outdata),CryGold4Web.eva.csvMatch.OperandsContentHandling):
        return toCSV(outObj.outdata)
    if type(outObj.outdata) is str:
        return outObj.outdata
    if type(outObj.outdata) is list:
        return str(outObj.outdata)
    return 'None'

@app.route('/')
def begin():
    argument = flask.request.args.get('arguments')
    if argument == None:
        prefilled = "pricecoins/XMG-BTC.csv mul pricecoins/btc-eur.csv 2018-01-01_00:00 2018-04-01_00:00"
    else:
        prefilled = str(argument)
    website = "<html><head></head><body><form action=\"/run\"> \
            <input id=\"0\" name=\"arguments\" size=\"35\" value=\""+prefilled+"\"><br> \
            <button type=\"submit\"> \
            give-Table</button></form><br> \
            <a href=\"/pricecoins.json\">files in pricecoins</a><br><a href=\"/amountcoins.json\">files in amountcoins</a><br> \
            <a href=\"/operations.json\">operations</a><br> \
            </body></html>"
    return website

@app.route('/run')
def home():
    #if "name" not in form or "addr" not in form:
        #a="<H1>Error</H1>"
        #b="Please fill in the name and addr fields."
        #c=str(form)
    #d=form.username
    #    return a+b+d
    #a="<p>name:"+ form["name"].value
    #b="<p>addr:"+ form["addr"].value
    argument = flask.request.args.get('arguments')
    wordsList = str(argument).split(' ')
    for word in wordsList[:1]:
            if os.path.isfile(word):
                if not is_safe_path('/opt/scripts/crycsv/pricecoins', word) and not is_safe_path('/opt/scripts/crycsv/amountcoins',word):
                    return 'One file exists, but is in the wrong path!'
    try:
        arg = '/blub/CryGold4Web.piii ' + argument
        outObj = CryGold4Web.getCmdParaManageObj(arg)
    except Exception as inst:
        exc_type, exc_obj, exc_tb = sys.exc_info()
#        del(exc_type, exc_value, exc_traceback)
        traceback_details = {
                                 'filename': exc_tb.tb_frame.f_code.co_filename,
                                 'lineno'  : exc_tb.tb_lineno,
                                 'name'    : exc_tb.tb_frame.f_code.co_name,
                                 'type'    : exc_type.__name__,
                                 #'message' : exc_value.message, # or see traceback._some_str()
                                }
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return "Command Parameter Error , Exception Type: "+str(type(inst))+" Args: "+str(inst.args) + \
        str(exc_type)+"<br>\n"+str(fname)+"<br>\n"+str(exc_tb.tb_lineno) + \
        '<br>\n'+str(argument)+'<br>\n'+str(traceback.format_exc())+'\n<br>'
    try:
        if issubclass(type(outObj.outdata),CryGold4Web.eva.csvMatch.OperandsContentHandling):
            return toCSV(outObj.outdata)
        if type(outObj.outdata) is str:
            return outObj.outdata
        if type(outObj.outdata) is list:
            return str(outObj.outdata)
        return 'None'
    except Exception as inst:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return "Output Error , Exception Type: "+str(type(inst))+" Args: "+str(inst.args) + \
        str(exc_type)+"\n"+str(fname)+"\n"+str(exc_tb.tb_lineno)


@app.route('/amountcoins.json')
def amount():
    return json.dumps(dirs('/opt/scripts/crycsv/amountcoins'))


@app.route('/pricecoins.json')
def price():
    return json.dumps(dirs('/opt/scripts/crycsv/pricecoins'))


@app.route('/operations.json')
def operations():
    return json.dumps(CryGold4Web.eva.operations.OpTypesHandling.getOperationList())
