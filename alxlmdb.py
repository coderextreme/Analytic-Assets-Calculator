#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
#os.environ['LMDB_FORCE_CFFI'] = None
import lmdb
import json
import time
import ccxt.async_support as ccxt

logger = logging.getLogger('lmdb-test')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('lmdb-Test.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


rootDatasDir = '/home/alex/workspace-noneclipse/crycsv/'


#lmdb.open('db-data-1',max_dbs=0)
#lmdb.Environment.begi
#txn = lmdb.Transaction
#txn.put(lmdb.VersionMismatchError('a','b'))
#print(str(txn.pop('a')))


def type_IntToByte(num):
    return num.to_bytes(10,'little')

def type_ToJsonToByte(val):
    try:
        return json.dumps(val).encode()
    except Exception as ex:
        logger.debug('type_ToJsonToByte: '+str(type(ex).__name__) + ' ' + str(ex.args))


def type_ByteToFromJson(bina):
    if type(bina) is memoryview:
        bina = bina.tobytes()
    if type(bina) is bytes or type(bina) is bytearray:
        return None if bina is None else json.loads(bina.decode('UTF-8'))
    else:
        if bina is None:
            return None
        else:
            raise TypeError('in Byte To FromJson Type is '+str(type(bina)))

def type_StrToByte(text):
    try:
        return str(text).encode()
    except Exception as ex:
        logger.debug('type_StrToByte: '+str(type(ex).__name__) + ' ' + str(ex.args))

def storeDdos(key,val):
    subfolder = 'ddos'
    if not type(key) is str:
        raise TypeError('wrong Types for storeExchMarkCurList key')
    if not type(val) is list:
        raise TypeError('wrong Types for storeExchMarkCurList val'+str(type(val)))
    with lmdb.Environment.begin(lmdb.Environment(rootDatasDir+subfolder+'/',max_dbs=0),write=True, buffers=True) as txn:
        try:
            txn.put(type_StrToByte(key), type_ToJsonToByte(val))
        except Exception as ex:
            logger.debug('txn.put: '+str(type(ex).__name__) + ' ' + str(ex.args))

def getDdos(key):
    subfolder = 'ddos'
    if not type(key) is str:
        raise TypeError('wrong Types for getExchMarkCurList')
    with lmdb.Environment.begin(lmdb.Environment(rootDatasDir+subfolder+'/',max_dbs=0),write=False, buffers=True) as txn:
        bina = txn.get(type_StrToByte(key))
        return type_ByteToFromJson(bina)

def storeExchMarkCurList(subfolder,key,val):
    if not type(key) is int:
        raise TypeError('wrong Types for storeExchMarkCurList key')
    if not type(val) is dict:
        raise TypeError('wrong Types for storeExchMarkCurList val'+str(type(val)))
    with lmdb.Environment.begin(lmdb.Environment(rootDatasDir+subfolder+'/',max_dbs=0),write=True, buffers=True) as txn:
        txn.put(type_IntToByte(key), type_ToJsonToByte(val))

def getExchMarkCurList(subfolder,key):
    if not type(key) is int:
        raise TypeError('wrong Types for getExchMarkCurList')
    with lmdb.Environment.begin(lmdb.Environment(rootDatasDir+subfolder+'/',max_dbs=0),write=False, buffers=True) as txn:
        bina =txn.get(type_IntToByte(key))
        return type_ByteToFromJson(bina)



def storeSTRINT(subfolder,key,val):
    if not type(key) is str or not type(val) is int:
        raise TypeError('wrong Types for storeSTRINT')
    with lmdb.Environment.begin(lmdb.Environment('/home/alex/workspace-noneclipse/crycsv/'+subfolder+'/',max_dbs=0),write=True, buffers=True) as txn:
        txn.put(str(key).encode(), val.to_bytes(10,'little'))
def getSTRINT(subfolder,key):
    with lmdb.Environment.begin(lmdb.Environment('/home/alex/workspace-noneclipse/crycsv/'+subfolder+'/',max_dbs=0),write=False, buffers=True) as txn:
        return txn.get(key.encode()).tobytes()

def storeSTRs(subfolder,key,val):
    with lmdb.Environment.begin(lmdb.Environment('/home/alex/workspace-noneclipse/crycsv/'+subfolder+'/',max_dbs=0),write=True, buffers=True) as txn:
        txn.put(str(key).encode(), str(val).encode())
def getSTRs(subfolder,key):
    with lmdb.Environment.begin(lmdb.Environment('/home/alex/workspace-noneclipse/crycsv/'+subfolder+'/',max_dbs=0),write=False, buffers=True) as txn:
        return bytes(txn.get(key.encode())).decode('UTF-8')


#storeDDOS('test',1234)
#print(str(getDDOS('test')))

def storeAllThatsCollected(exchange,market,itemdict):
    if issubclass(type(exchange),ccxt.Exchange):
        if type(itemdict) is dict:
            subfolder = 'chartdata/'+str(type(exchange).__name__)+'/'+str(market['symbol']+'/')
            if not os.path.exists(rootDatasDir+subfolder):
                os.makedirs(rootDatasDir+subfolder)
            storeExchMarkCurList(subfolder,int(time.time()),itemdict)
        else:
            raise ValueError('not a dict')
    else:
        raise ValueError('not an Exchange')
