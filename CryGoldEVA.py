#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import LibCrygoldEVA as eva
import sys
import logging
logger = logging.getLogger('PyCryGold')
logger.setLevel(logging.DEBUG)
#blub = eva.csvTimed().run()
#if len(sys.argv)>4:
#    blub.toFile(sys.argv[4])
#else:
#    blub.chartDisplayForNow()
logger.debug("CmdParMan create from CryGold4Web")
blub = eva.CommandParameterManaging(sys.argv)



#print (str(blub.getParameterTypes()))
#if blub.parse():
#blub.exec()


#eva.multipleChartDatas(sys.argv[1],eva.csvMatch.types.crygold,None,None,sys.argv[2],eva.csvMatch.types.crygold,None,None).showChart()
