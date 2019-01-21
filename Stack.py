#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import operations
import CursorNToken
import logging
from csvMatch import join2CSVs

logger = logging.getLogger('PyCryGold')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('PyCryGold.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

class Stack():
    def __init__(self):
        self._stack = []

    def isEmpty(self):
        if self._stack == []:
            return True
        else:
            return False
    def isOneInside(self):
        if len(self._stack) == 1:
            return True
        else:
            return False


    def push(self, el):
        if type(el) is CursorNToken.Token:
            if not self.isEmpty:
                if (type (self._stack[-1]) is operations.INumberOperator \
                and el.isNumber ) or (type (self._stack[-1]) \
                is operations.IOperateCharts and el.isGraph):
                    self._stack.append(el)
                else:
                    raise "alx wrong inserted"
            else:
                if el.isNumber or el.isGraph:
                    self._stack.append(el)
                else:
                    raise "alx first insert must be data"
        else:
            raise "alx push is not a token"

    def pop(self):
        op = []
        #print('0')
        #if len(self._stack) > 2:
        ##    logger.debug('LenOpni A is: '+str(len(self._stack)))
        #    logger.debug('LenOpni B is: '+str(self._stack[-3].token))
        #    logger.debug('LenOpni C is: '+str(self._stack[-3].isTypeAsString()))
        #    #if self._stack[-3].isGraphOperation():
        #    logger.debug('LenOpni D is: '+str(self._stack[-3].token.LenOperands()))
        #if len(self._stack) > 4:
        #    logger.debug('LenOpni E1 is: '+str(len(self._stack)))
        #    logger.debug('LenOpni E is: '+str(self._stack[-5].token.LenOperands()))
        if CursorNToken.Token(self.top()).isOperandsContentHandling \
        or CursorNToken.Token(self.top()).isNumber:
            #print(str(type(self.top().isOpTypesHandling())))
            print('1')
            op.append(self._stack.pop())
            #logger.debug('Result is: '+str(result.OperandsContentHandling.toPyStdStructure()[-1][-1]))
            if self.isEmpty():
                if CursorNToken.Token(op[0]).isOperandsContentHandling:
                    #print('xxx'+str(op[0].token))
                    return op[0]
            #if CursorNToken.Token(self.top()).isOperandsContentHandling \
            #or CursorNToken.Token(self.top()).isNumber \
            #or self.top().isGraphOperation:
            print('1b')
            print(str(self.top().isOperateWhatEver))
            if CursorNToken.Token(self.top()).isOperandsContentHandling \
            or CursorNToken.Token(self.top()).isNumber:
                print('2')
                op.append(self._stack.pop())
                #print(str(self.top()))
                if not self.isEmpty() and self.top().isOperateWhatEver:
                    print('3')
                    #print('3')
                    op.append(self._stack.pop())
                    #logger.debug('OP D: '+str(op[2].token))
                    #logger.debug('LenOpn was: '+str(op[2].token.LenOperands()))
                    print("Dogen is "+str(op[2].token))
                    op[2].token.addOperand(op[1])
                    op[2].token.addOperand(op[0])
                    #logger.debug('Op is: '+str(op[2].token))
                    #logger.debug('LenOpn is: '+str(op[2].token.LenOperands()))
                    #logger.debug('Opn01 is: '+str(op[0].token))
                    #logger.debug('Opn0 is: '+str(op[0].token.toPyStdStructure()[-1][-1]))
                    #logger.debug('Opn1 is: '+str(op[1].token[-1]))
                    #logger.debug('Opn1 is: '+str(op[1].token.toPyStdStructure()[-1][-1]))
                    result = op[2].token.execute().getResult()
                    self.push(result)
                    #logger.debug('size: '+str(len(self._stack)))
                    #logger.debug('Result is: '+str(result.token.toPyStdStructure()[-1][-1]))
                    #logger.debug('Result is: '+str(result.token))
                    return result
            #elif self.top().isOperateWhatEver and type(self.top()) is operations.joinOp:
                else:
                    #raise ValueError("Programming discontinued here")
            #elif self.top().isOperateWhatEver:
                    try:
                        print('one op: '+str(op[-1]._token.operation))
                        if op[-1]._token.operation == operations.calcStackOp.negative:
                            op.append(CursorNToken.Token(float(-1)))
                            op[1].token.addOperand(op[2])
                            op[1].token.addOperand(op[0])
                        elif op[-1]._token.operation == operations.calcStackOp.same:
                            #op.append(CursorNToken.Token(op[0]))
                            op[1].token.addOperand(op[0])
                            op[1].token.addOperand(op[0])
                        #else:
                    except:
                        raise ValueError("In Calc Stack Operation has only one operand, but is not meant to be with one operand")
                    #op.append(self._stack.pop())
                    #print(str(op[2].token))
                    result = op[1].token.execute().getResult()
                    self.push(result)
                    print("x")
                    return result
        raise ValueError("error 99")


    def top(self):
        if not self.isEmpty():
            return self._stack[-1]
        else:
            return None
