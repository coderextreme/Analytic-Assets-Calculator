#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import LibCrygoldEVA as eva
import logging

logger = logging.getLogger('PyCryGold')
logger.setLevel(logging.DEBUG)

def getCmdParaManageObj(parameters):
    if parameters[-1] != ' ':
        parameters += ' '
    parameters += 'variable'
    para = parameters.split(' ')
    logger.debug("CmdParMan create from CryGold4Web")
    blub = eva.CommandParameterManaging(para)
    return blub
