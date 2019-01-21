#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ccxt.async_support as ccxt
from types import ModuleType
import sys, inspect
import time
import asyncio
import logging
import ssl
import alxlmdb
import collections
import math

exchanges = []

def setLogger(val=None):
    if val == 'values':
        logger = logging.getLogger('chartValues')
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('chartValues.log')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    else:
        logger = logging.getLogger('getCharts')
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('getCharts.log')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger

logger = setLogger()
vlogger = setLogger('values')

# Programmieren, dass: alles angezeigt, und schlüsselwörter davor:
# also währung1/währung2 böse: börsenname
# zeilenumbruch zwischen währungssachen


async def eachExchange(name,ExchClass):
    global exchanges
    if inspect.isclass(ExchClass):
        if issubclass(ExchClass,ccxt.Exchange) and ExchClass.__name__ != "Exchange":# and obj.__name__ != "_1broker" and obj.__name__ != "_1btcxe":
            try:
                logger.debug('name: '+str(name))
                exchange = ExchClass({'verbose': False,'timeout':15000, 'rateLimit': 8000})
                #try:
                #    await a
                #except TypeError:
                #    return None
                #logger.debug('exchange: '+ExchClass.__name__)
                #future = asyncio.Future()
                #asyncio.ensure_future(slow_operation(future))
                #await asyncio.wait_for(exchange.load_markets(),timeout=16000)
                await exchange.load_markets()
                    #b = a.load_markets()
                    #time.sleep(rateLimit(a,obj))
            except ccxt.ExchangeError:
                logger.debug('exchange: ExchangeError')
                return None
            except ccxt.DDoSProtection:
                logger.debug('exchange: DDOS...')
                return None
            except ccxt.ExchangeNotAvailable:
                logger.debug('exchange: not available')
                return None
            except ccxt.RequestTimeout:
                logger.debug('exchange: timeout')
                return None
            else:
                exchanges.append([exchange,ExchClass])
            #except:
            #    logger.debug('exchange: ?')
            #    return None
            finally:
                pass
                #await exchange.market.close()
                #await exchange.close()
            return exchange,ExchClass
    return None

async def alltogether():
    global exchanges
#    loop = asyncio.new_event_loop()
#    asyncio.set_event_loop(loop)
    try:
        #await asyncio.wait_for(asyncio.gather(
        await asyncio.gather(
            #*[eachExchange(name,ExchClass) for name, ExchClass in inspect.getmembers(ccxt)],timeout=31000)
            *[await eachExchange(name,ExchClass) for name, ExchClass in inspect.getmembers(ccxt)]
        )
    except asyncio.TimeoutError:
        pass
        #p.kill()
        #await p.communicate()
    except:
        pass
    finally:
        pass
        #loop.close()
    #await asyncio.sleep(31000)
    #logger.debug('amount: '+str(len(exchanges)))
    exchanges = list(filter(lambda exchangesObjNclass: exchangesObjNclass[0] != None, exchanges))
    #print(str(exchanges))
    logger.debug('amount: '+str(len(exchanges)))
    return exchanges
    #for exchange in exchanges:
    #    exchange.close()
#print_classes()

#hitbtc = ccxt.hitbtc({'verbose': False})
##hitbtc_markets = hitbtc.load_markets()
#
##print(str(ccxt.Exchange.market_ids))
#u = hitbtc.fetch_markets()[-1]['symbol']
#print(str(u))
#n = hitbtc.fetch_ticker(u)
#print(str(n))
#for k,i in n.items():
#    if str(i)[0].isdigit():
#        print(str(k)+' '+str(i))

# GLEICH REDIS!

#def fetchMarkets(exchangeObj):
#def HandleDdosProtectionEachExchange(exchangeObj,ms):



async def eachMarketItem(exchange,market,key,item,itemdict):
    if str(item)[0].isdigit():
        vlogger.debug(str(type(exchange).__name__)+' '+str(market['symbol'])+' '+str(key)+' '+str(item))
        itemdict[key] = item

def getWaitSeconds(exchange):
    endu = get_Endurances(exchange)
    return 1 * math.pow(2,(endu[0]-1)) * math.pow(0.8,(endu[1]-1))

async def eachMarket(exchange,market,waitsec,DdosHappend=[]):
    itemdict = dict()
    try:
        #logger.debug('entry giveValuesFromExchange: for try2')
        if issubclass(type(market),collections.Mapping):
            await asyncio.sleep(waitsec)
            n = await exchange.fetch_ticker(market['symbol'])
            [await eachMarketItem(exchange,market,k,i,itemdict) for k,i in n.items()]
            DdosHappend.append(False)
            alxlmdb.storeAllThatsCollected(exchange,market,itemdict)
            #time.sleep(wait_)
        else:
            logger.debug('market is not a dict'+str(type(market)))
    except ccxt.ExchangeError:
        logger.debug('market ticker exchange '+type(exchange).__name__ +' error')
        pass
    except ccxt.ExchangeNotAvailable:
        logger.debug('market ticker exchange '+type(exchange).__name__ +' not available')
        pass
    except ccxt.DDoSProtection:
        logger.debug('market ticker exchange '+type(exchange).__name__ +' DDoSProtection')
        DdosHappend.append(True)
        return await ddosRetryTicker(exchange,market,None,DdosHappend)
    except ccxt.RequestTimeout:
        logger.debug('market ticker exchange '+type(exchange).__name__ +' timeout')
        DdosHappend.append(True)
        return await ddosRetryTicker(exchange,market,None,DdosHappend)
    except KeyError:
        logger.debug('market ticker exchange '+type(exchange).__name__ +' key error')
        pass
    except Exception as ex:
        logger.debug('market exchange '+type(exchange).__name__ +' else error '+str(type(ex).__name__) + ' ' + str(ex.args))
        pass
    except:
        logger.debug('market else exchange '+type(exchange).__name__ +' error ')
        pass
    else:
        return itemdict
    return None

def DoublePolling(exchange,ddosSleep=False):
    #logger.debug('DoublePolling1 '+str(type(exchange).__name__)+' '+str(ddosSleep))
    n = 3 if ddosSleep else 0
    stored = get_Endurances(exchange)
    stored[0+n] += 1
    alxlmdb.storeDdos(type(exchange).__name__, stored)
    logger.debug('DoublePolling '+str(type(exchange).__name__)+' '+str(stored))
    return stored

def TwentyPercentLessPolling(exchange,ddosSleep=False):
    n = 3 if ddosSleep else 0
    stored = get_Endurances(exchange)
    stored[1+n] += 1
    if stored[1+n] >= 4:
        if stored[0+n] > 1:
            stored[0+n] -= 1
        stored[1+n] = 1
        stored[2+n] += 1
    alxlmdb.storeDdos(exchange, stored)

def get_Endurances(exchange):
    try:
        stored = alxlmdb.getDdos(type(exchange).__name__)
        if stored is None:
            logger.debug('stored is none: ')
            stored = [1,1,1,1,1,1]
            alxlmdb.storeDdos(type(exchange).__name__, stored)
            logger.debug('stored between store and getting stored: ')
            stored = alxlmdb.getDdos(type(exchange).__name__)
            if stored is None:
                raise TypeError('Alx did Wrong!')
        else:
            logger.debug('stored is not none: '+str(stored))
    except Exception as ex:
        logger.debug('stored not: '+str(type(ex).__name__) + ' ' + str(ex.args))
        stored = [1,1,1,1,1,1]
    finally:
        logger.debug('waittimes: '+str(type(exchange).__name__)+' '+str(stored))
    return stored

async def ddosRetry(exchange,DdosHappend):
    #logger.debug('DdosHappend: '+str(DdosHappend))
    endu = DoublePolling(exchange,True) if DdosHappend[-1] else get_Endurances(exchange)
    if len(DdosHappend) >= 2:
        if not DdosHappend[-2]:
            endu = DoublePolling(exchange,False)
    waitForNextDdosRetry = 1 * math.pow(2,(endu[3]-1)) * math.pow(0.8,(endu[4]-1))
    logger.debug('because of DDoSProtection waited for '+str(type(exchange).__name__)+': '+str(endu)+' DdosHappend: '+str(DdosHappend[-2:-1])+' waitForNextDdosRetry:'+str(waitForNextDdosRetry))
    await asyncio.sleep(waitForNextDdosRetry)

async def ddosRetryExchange(exchangen,sett,DdosHappend):
    await ddosRetry(exchange,DdosHappend)
    return await giveValuesFromExchange(exchange,sett,DdosHappend)

async def ddosRetryTicker(exchange,market,waitsec,DdosHappend):
    await ddosRetry(exchange,DdosHappend)
    return await eachMarket(exchange,market,getWaitSeconds(exchange),DdosHappend)


def endurancePolling(stored):
    return stored[0]

async def giveValuesFromExchange(exchange,sett,DdosHappend=[]):
    #logger.debug('entry giveValuesFromExchange')
    #exchange = ExchClass({'verbose': False})
    waitsec = getWaitSeconds(exchange)
    try:
        #exchange = ExchClass({'verbose': False,'timeout':15000, 'rateLimit': 8000})
        #logger.debug('entry giveValuesFromExchange try1')
        markets = await exchange.fetch_markets()
        await asyncio.sleep(waitsec)
        #logger.debug('entry giveValuesFromExchange try1a')
        #logger.debug('entry giveValuesFromExchange try1b '+str(markets))
        #ccxt.Exchange.fetch_markets.__dict__.items():
        [await eachMarket(exchange,market,waitsec) for market in markets]
        DdosHappend.append(False)
        #logger.debug('entry giveValuesFromExchange try1b')
    except ccxt.ExchangeNotAvailable:
        logger.debug('exchange '+type(exchange).__name__ +' not avail')
        pass
    except ccxt.ExchangeError:
        logger.debug('exchange '+type(exchange).__name__ +' ExchangeError')
        pass
    except ccxt.DDoSProtection:
        logger.debug('exchange '+type(exchange).__name__ +' DDoSProtection')
        DdosHappend.append(True)
        return await ddosRetryExchange(exchange,sett,DdosHappend)
    except ccxt.RequestTimeout:
        logger.debug('exchange '+type(exchange).__name__ +' timeout')
        DdosHappend.append(True)
        return await ddosRetryExchange(exchange,sett,DdosHappend)
    except Exception as ex:
        logger.debug('exchange '+type(exchange).__name__ +' else error '+str(type(ex).__name__) + ' ' + str(ex.args))
        pass
        #else:
        #    pass
    except:
        logger.debug('exchange '+type(exchange).__name__ +' else error ')
        pass
    finally:
        sett.remove([exchange, type(exchange)])
        logger.debug('Exchanges still inside: '+str(len(sett)))
        await exchange.close()

# GLEICH REDIS!
#def rateLimit(exchange):
#    logger.debug('entry rateLimit')
#    #exchange = ExchClass({'verbose': False})
#    #async with ExchClass({'verbose': False}) as exchange:
#    if type(exchange).__name__ == 'bitfinex' or type(exchange).__name__ == 'bitfinex2':
#        limit = 40
#    else:
#        limit = exchange.rateLimit / 1000
#        #print(str(ExchClass.__name__)+' '+str(limit))
#        #time.sleep(limit)
#    #await exchange.close()
#    #await exchange
#    return limit

loop = asyncio.get_event_loop()
try:
    sett = loop.run_until_complete(alltogether())
except Exception as ex:
    logger.debug('list exchanges else error '+str(type(ex).__name__) + ' ' + str(ex.args))
    pass
except:
    pass
finally:
    pass
#    pass
    #asyncio.sleep(31000)
    #loop.close()
#print(str(exchanges))
#list_ = alltogether()
logger.debug('go on!')
async def bla(sett):
    try:
        logger.debug('trying')
        #loop.run_until_complete(asyncio.gather(
        await asyncio.gather(
            *[giveValuesFromExchange(exchange,sett) for exchange,ExchClass in sett]
        )
        logger.debug('trying end')
    except Exception as ex:
        logger.debug('each all exchanges else error '+str(type(ex).__name__) + ' ' + str(ex.args))
        pass
    finally:
        pass

#loop = asyncio.new_event_loop()
#asyncio.set_event_loop(loop)
loop.run_until_complete(bla(sett))
#asyncio.gather(bla(list_))
#asyncio.sleep(15000000)
#loop.close()
#loop = asyncio.new_event_loop()
#asyncio.set_event_loop(loop)
#try:
#loop.create_task(bla(list_))
#finally:
#    loop.close()

#print(str(hitbtc.fetch_markets()[-1]['symbol']))
#ccxt.Exchange.currency
#print(i.symbols)

#for b in ccxt.exchanges:
#hitbtc = ccxt.hitbtc({'verbose': True})
#hitbtc_markets = hitbtc.load_markets()
#print(hitbtc.id, hitbtc_markets)
