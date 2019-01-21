#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ccxt
from types import ModuleType
import sys, inspect
import time

# Programmieren, dass: alles angezeigt, und schlüsselwörter davor:
# also währung1/währung2 böse: börsenname
# zeilenumbruch zwischen währungssachen

def alltogether():
    flag = False
    flag2 = False
    #for name, obj in inspect.getmembers(sys.modules[__name__]):
    for name, obj in inspect.getmembers(ccxt):
        if inspect.isclass(obj):
            if issubclass(obj,ccxt.Exchange) and obj.__name__ != "Exchange" and obj.__name__ != "_1broker" and obj.__name__ != "_1btcxe":
#                obj.__class__ = ccxt.Exchange
#                ccxt.Exchange.currencies
                a = obj({'verbose': False})
                try:
                    b = a.load_markets()
                    time.sleep(rateLimit(a,obj))
                except ccxt.ExchangeError:
                    continue
                except ccxt.DDoSProtection:
                    continue
                except ccxt.ExchangeNotAvailable:
                    continue
                except ccxt.RequestTimeout:
                    continue
#                #if not b is NoneType:
                #print(str(obj.__name__))
                #print(obj().currencies)
                if flag:
                    flag2 = True
                if obj.__name__ == "bxinth":
                    flag = True
                if flag:
                    giveValuesFromExchange(a,rateLimit(a,obj))
#                rateLimit(a,obj)

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
def giveValuesFromExchange(exchange,wait_,heading=False):
    try:
        for market in exchange.fetch_markets():
            try:
                n = exchange.fetch_ticker(market['symbol'])
                for k,i in n.items():
                    if str(i)[0].isdigit():
                        print(str(k)+' '+str(i))
                time.sleep(wait_)
            except ccxt.ExchangeError:
                pass
            except ccxt.ExchangeNotAvailable:
                pass
            except ccxt.RequestTimeout:
                pass
            except KeyError:
                pass
    except ccxt.ExchangeNotAvailable:
        pass
    except ccxt.ExchangeError:
        pass
    except ccxt.RequestTimeout:
        pass

# GLEICH REDIS!
def rateLimit(exchange,exchClass):
    if exchClass.__name__ == 'bitfinex' or exchClass.__name__ == 'bitfinex2':
        limit = 40
    else:
        limit = exchange.rateLimit / 1000
    print(str(exchClass.__name__)+' '+str(limit))
    #time.sleep(limit)
    return limit

#ccxt.Exchange.safe_string^
alltogether()
#print(str(hitbtc.fetch_markets()[-1]['symbol']))
#ccxt.Exchange.currency
#print(i.symbols)

#for b in ccxt.exchanges:
#hitbtc = ccxt.hitbtc({'verbose': True})
#hitbtc_markets = hitbtc.load_markets()
#print(hitbtc.id, hitbtc_markets)
