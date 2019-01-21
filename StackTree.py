#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import subprocess
import time
import datetime
import csv
from enum import IntEnum
import statistics
import math
import LibCrygoldEVA
import logging
from operations import OpTypesHandling
from operations import calcStackOp
import os

logger = logging.getLogger('PyCryGold')
logger.setLevel(logging.DEBUG)


class StackTree():
    def __init__(self,cmdParaMan):
        #restTypes = cmdParaMan.restTypes
        self.cmdParaMan = cmdParaMan
        self.tree1 = [None,[],[]] # 3 Elemente: Vater, Kinder, Eigenschaften

    @staticmethod
    def __isBrackets(text):
        return ( text[0]=="(" and text[-1]==")" ) or ( text[0]=="[" and text[-1]=="]" ) or ( text[0]=="{" and text[-1]=="}" )

    @staticmethod
    def __OperandTypesList():
        return [LibCrygoldEVA.ParameterTypes.FileExistingOrReservedWord, \
                LibCrygoldEVA.ParameterTypes.number, \
                LibCrygoldEVA.ParameterTypes.FlattenType, \
                 LibCrygoldEVA.ParameterTypes.BracketOpen]
                #or obj == LibCrygoldEVA.ParameterTypes.BracketClose

    @staticmethod
    def __isOperand(obj):
        return obj in StackTree.__OperandTypesList()

    @staticmethod
    def __isCsvFileExisting(text):
        if os.path.isfile(text) and len(text) >= 4:
            return text[-4:] == ".csv"
        return False
    @staticmethod
    def __isOperator(obj):
        return obj in [LibCrygoldEVA.ParameterTypes.operationWithTwoOperands, \
            LibCrygoldEVA.ParameterTypes.operationWithThreeOperands, \
            LibCrygoldEVA.ParameterTypes.operationWithOneOperand]

#    def _parseBracket(self,restTypes,parameterList,calcStack,bracket,weiredOperandsCounter,count,type_ ):
#        if type_ == LibCrygoldEVA.ParameterTypes.FileExistingOrReservedWord and count == 0 \
#        and self.__isOperator(restTypes[count+1]) \
#        and self.__isOperand(restTypes[count+2]):
#            self.cmdParaMan.outdata += "<br>\nFirst Calculation"
#            calcStack.append(parameterList[count+1])
#            calcStack.append(self.cmdParaMan.getOneStepSeconds(parameterList[count+1]))
#            op = OpTypesHandling.EnumKeyByStrKey(parameterList[count+2])
#            if op is None:
#                self.cmdParaMan.outdata += "<br>\nOperation == None :" + str(parameterList[count+2])
#                return False,restTypes,calcStack,bracket,weiredOperandsCounter
#            calcStack.append(op)
#            if restTypes[count+2] == LibCrygoldEVA.ParameterTypes.BracketOpen:
#                calcStack.append('()')
#                bracket = count+2
#            else:
#                ##printself.cmdParaMan.outdata)
#                ##printstr(restTypes))
#                ##printstr(parameterList))
#                calcStack.append(parameterList[count+3])
#            if restTypes[count+2] == LibCrygoldEVA.ParameterTypes.FlattenType:
#                calcStack.append(self.cmdParaMan.getOneStepSeconds(parameterList[count+1]))
#            else:
#                ##print'xx '+str(parameterList[count+3]))
#                calcStack.append(self.cmdParaMan.getOneStepSeconds(parameterList[count+3]))
#            weiredOperandsCounter+=2
#            logger.debug('First Step: '+str(calcStack))
#            self.cmdParaMan.outdata += "<br>\nFirst + 2 Parameter Successful parsed "+str(calcStack)
#            #['pricecoins/XMG-BTC.csv', 300, 'pricecoins/XMG-BTC.csv', <calcStackOp.mul: 1>, 300]
#            #print"abc1 "+str(calcStack))
#            return True,restTypes,calcStack,bracket,weiredOperandsCounter
#        elif count == 0:
#            if restTypes[count] == LibCrygoldEVA.ParameterTypes.BracketOpen:
#                calcStack.append('()')
#                #print"abc1b "+str(calcStack))
#                calcStack.append(0)
#                #print"abc1b "+str(calcStack))
#                bracket = count
#                return True,restTypes,calcStack,bracket,weiredOperandsCounter
#            else:
#                logger.debug('First 3 Things are not a calculation')
#                self.cmdParaMan.outdata += "<br>\nFirst 3 Things are not a calculation"
#                self.cmdParaMan.outdata += "<br>\nThey are: "+str(restTypes)
#                return False,restTypes,calcStack,bracket,weiredOperandsCounter
#        if count > 0 and count + 1 < len(restTypes) and self.__isOperator(type_) \
#        and self.__isOperand(restTypes[count+1]):
#            self.cmdParaMan.outdata += "<br>\nAnother Calculation"
#            op = OpTypesHandling.EnumKeyByStrKey(parameterList[count+1])
#            if op == None:
#                self.cmdParaMan.outdata += "<br>\nSecond + x' Operation == None"
#                return False,calcStack,restTypes,tree1
#            calcStack.append(op)
#            #printself.cmdParaMan.outdata)
#            if restTypes[count+1] == LibCrygoldEVA.ParameterTypes.BracketOpen:
#                calcStack.append('()')
#                bracket = count+1
#            else:
#                calcStack.append(parameterList[count+2])
#            logger.debug('Filename: '+str(parameterList[count+2]))
#            if restTypes[count+1] == LibCrygoldEVA.ParameterTypes.FlattenType:
#                if self.__isCsvFileExisting(parameterList[count]):
#                    calcStack.append(self.cmdParaMan.getOneStepSeconds(parameterList[count]))
#                else:
#                    calcStack.append(0)
#            else:
#                calcStack.append(self.cmdParaMan.getOneStepSeconds(parameterList[count+2]))
#            weiredOperandsCounter += 1
#            self.cmdParaMan.outdata += "<br>\nSecond + x Operand Successful parsed"
#            ##print'b')
#            return True,restTypes,calcStack,bracket,weiredOperandsCounter
#        else:
#            self.cmdParaMan.outdata += "<br>\nSecond + x Operand wrong"
#        self.cmdParaMan.outdata += "<br>\n Loop Conditions not fullfilled, restTypes= "+str(restTypes)
#        return False,restTypes,calcStack,bracket,weiredOperandsCounter

#    def _parseBringTokenToParseIt(self,restTypes,parameterList,calcStack,bracket,weiredOperandsCounter,count,type_ ):
#        if type_ == LibCrygoldEVA.ParameterTypes.FileExistingOrReservedWord and count == 0 \
#        and self.__isOperator(restTypes[count+1]) \
#        and self.__isOperand(restTypes[count+2]):
#            firstCalcInBracket = True
#        elif count == 0 and restTypes[count] == LibCrygoldEVA.ParameterTypes.BracketOpen:
#            calcStack.append('()')
#            calcStack.append(0)
#            bracket = count
#            return True,restTypes,calcStack,bracket,weiredOperandsCounter
#        elif count > 0 and count + 1 < len(restTypes) and self.__isOperator(type_) \
#        and self.__isOperand(restTypes[count+1]):
#            firstCalcInBracket = False
#        else:
#            logger.debug('Things are not a calculation')
#            self.cmdParaMan.outdata += "<br>\nThings are not a calculation"
#            self.cmdParaMan.outdata += "<br>\nThey are: "+str(restTypes)
#            return False,restTypes,calcStack,bracket,weiredOperandsCounter
#
#        if firstCalcInBracket == True:
#            self.cmdParaMan.outdata += "<br>\nFirst Calculation"
#            calcStack.append(parameterList[count+1])
#            calcStack.append(self.cmdParaMan.getOneStepSeconds(parameterList[count+1]))
#            delta = 1
#        else:
#            delta = 0
#
#        op = OpTypesHandling.EnumKeyByStrKey(parameterList[count+1+delta])
#        if op is None:
#            self.cmdParaMan.outdata += "<br>\nOperation == None :" + str(parameterList[count+1+delta])
#            return False,restTypes,calcStack,bracket,weiredOperandsCounter
#        calcStack.append(op)
#
#        for amountMoreOperands in range(0,OpTypesHandling.calcStackOp.amountOperands(op)-2):
#            bracketsteps = 0
#            bracketopened = False
#            amountMoreOperandsB = amountMoreOperands + bracketsteps
#            if restTypes[count+1+delta+amountMoreOperandsB] == LibCrygoldEVA.ParameterTypes.BracketOpen:
#                calcStack.append('()')
#                bracket = count+1+delta+amountMoreOperandsB
#                bracketopened = True
#            if bracket is None:
#                # add 2nd 3rd etc operand:
#                calcStack.append(parameterList[count+2+delta+amountMoreOperandsB-bracketsteps])
#                # this is for clearify stepseconds number
#                if restTypes[count+1+delta+amountMoreOperandsB-bracketsteps] == LibCrygoldEVA.ParameterTypes.FlattenType:
#                    if self.__isCsvFileExisting(parameterList[count-delta-amountMoreOperandsB-bracketsteps]):
#                        calcStack.append(self.cmdParaMan.getOneStepSeconds(parameterList[count-delta-amountMoreOperandsB-bracketsteps]))
#                    else:
#                        calcStack.append(0)
#                else:
#                    calcStack.append(self.cmdParaMan.getOneStepSeconds(parameterList[count+2+delta+amountMoreOperandsB-bracketsteps]))
#            if restTypes[count+1+delta+amountMoreOperandsB] == LibCrygoldEVA.ParameterTypes.BracketClose:
#                bracketopened = False
#                bracketsteps += 1
#            if bracketopened:
#                bracketsteps += 1
#                # zählt hoch bei '(' 'einElement' ')' auf zahl 3,
#                # er wäre jetzt einen schritt weiter und muss nun aber 3 fach
#                # weiter gehen deshalb +3
#                # Ich muss hier später berücksichtigen dass ab operand 2 auch
#                # klammern ineinander sein können, was der code nicht
#                # berücksichtigt, wenn ein zweiter dritter operand eine klammer
#                # hat, berücksichtigt das hier nicht, pro operation mit ihren
#                # operanden
#                # Es funktioniert auch nicht, dass berücksichtigt wird wenn eine
#                # operation mit anzahlen von operanden: Also es funktioniert
#                # dass ein operand eine Klammer sei kann, aber vielleicht nicht,
#                # dass mehrere Operanden eine Klammer SIND
#
#                # Lösung, versucht einfach: Ich mache aus 2 nun 3
#                # Klassenfunktionen: statt pro Bracket und Operation:
#                # Fkt machen, die liste aus Brackets in Op gestaltet,
#                # Fkt, die das als Grundlage nutzt um einfacher pro Op zu parsen
#                # Fkt, die pro Bracket parseAll startet
#
#                # ParseAll ist pro Bracket
#                # ParseDetermineBracket ist bestimmen der Bracket
#                # _parseBringTokenToParseIt macht eine Op
#                # ich brauche festellen von mehreren Brackets pro Op
#
#                # Ablauf ist im Moment so, dass ParseAll jedes Token durch geht,
#                # wobei jedoch _parseBringTokenToParseIt macht, dass immer
#                # vor gesprungen wird je Op, und nach jeder Op wird bisher die
#                # letzte Bracket als ganzes Verstanden mit ihren Unterbrackets,
#                # aber ich möchte alle Brackets in einer Op einbeziehen
#
#                # Unterbrackets feststellen: macht schon die ParseDetermineBracket
#                # brauche ich aber auch um genau dieser selben Fkt mit zu geben
#                # und fest zu stellen, wenn es auf gleicher Ebene noch eine
#                # Bracket gibt, da beißt sich die Katze in den Schwanz!
#
#                # Jetzt stelle ich gerade fest, dass bei Bracket detektion mit
#                # return true die Operation frühzeitig beendet wird, dass das
#                # beahndelt werden kann, also wurde es doch schon richtig
#                # korrekt einprogrammiert
#
#                # Aber wie habe ich dann programmiert, dass weiter geparsed wird
#                # pro Bracket: weiredOperandsCounter geht erst hoch nach Ende des zweiten
#                # Operanden, so lange wird jedes Token untersucht und der
#                # Prozedur die pro Operation mit ihren Operanden durch geht,
#                # wird ohne jump einfach nur immer wieder das nächste Token mit
#                # gegeben aber auch die schleifenzählvariable, die alle token
#                # bestimmt als index des arrays der Parameter und der
#                # Parametertypen, dass die 2 arrays das array bestimmen der
#                # token der calc liste
#
#                # wenn pro entdeckter klammer die abarbeitung pro Op mit Opnds
#                # einfach mit True Okay abgebrochen wird, dann muss diese auch
#                # weiter gehen können, und zwar dann, immer wenn eine klammer
#                # pro Opnd behandelt wurde mit der BracketS Prozedur
#
#                # Ich brauche eine Prozedur pro Token, der die Situation kurz
#                # mitgegeben wird, und eine Prozedor pro ganze Op mit Opnds
#                # die Op die Pro Op mit Opnds ist, bricht immer mit True bei
#                # Klammer auf Fund ab, die neue Prozedur pro Token wird je ggf
#                # durch die Pro Op aufgerufen und eine Var stellt dann fest, ob
#                # ganze Op durch ist, eine var stellt fest wie viele token noch
#                # durch müssen bis für fkt die pro token ist, die var die sagt,
#                # dass alle token für op mit deren opnds durch ist, wird
#                # überprüft in der fkt die klammern behandelt
#
#                # der prozedur pro token muss mit gegeben werden: token, nr des
#                # tokens, was okay sein wird, was nicht okay sein wird, ggf was
#                # im zweifelsfall getan werden muss
#        #finished
#        weiredOperandsCounter+=1+delta+amountMoreOperands
#        self.cmdParaMan.outdata += "<br>\nPart Calculation Parameters Successful parsed "+str(calcStack)
#        return True,restTypes,calcStack,bracket,weiredOperandsCounter

    def _parseOneToken(self,paraToken,typeToken,calcStack,tokenShallBeList,count):
        #weiredOperandsCounter größer null damit nicht geparsed wenn op mit opnd schon abgearbeitet wird und
        #zur nächsten Op mit ihren Opnds gesprungen werden kann
        bracket = None
        if typeToken in tokenShallBeList:
            if self.__isOperator(typeToken):
                op = OpTypesHandling.EnumKeyByStrKey(paraToken)
                if op is None:
                    self.cmdParaMan.outdata += "<br>\nOperation == None :" + str(paraToken)
                    return False,calcStack,bracket
                calcStack.append(op)
            elif typeToken == LibCrygoldEVA.ParameterTypes.BracketOpen:
                calcStack.append('()')
                calcStack.append(0)
                bracket = count
            elif self.__isOperand(typeToken):
                calcStack.append(paraToken)
                if typeToken == LibCrygoldEVA.ParameterTypes.FileExistingOrReservedWord and os.path.isfile(paraToken):
                    calcStack.append(self.cmdParaMan.getOneStepSeconds(paraToken))
                else:
                    calcStack.append(0)
            elif typeToken == LibCrygoldEVA.ParameterTypes.BracketClose:
                raise ValueError("Bracket Close is nothing to be here expected, though is to be treated before")
            else:
                print('Token: '+str(paraToken)+'of Type: '+str(typeToken))
                raise ValueError("Token is one the one hand like it should be, but on the other it is none it could be")
            self.cmdParaMan.outdata += 'Token Parse Success of Token: '+str(paraToken)+'of Type: '+str(typeToken)
            return True,calcStack,bracket
        self.cmdParaMan.outdata += 'Token Parse Failsure of Token: '+str(paraToken)+'of Type: '+str(typeToken)
        return False,calcStack,bracket
        pass

    def _parseBringTokenToParseIt(self,restTypes,parameterList,calcStack,bracket,weiredOperandsCounter,count,type_ ):
        if weiredOperandsCounter < 0: # -1 when first operand at all or when second operand
            tokenresult = self._parseOneToken(parameterList[count+1],type_,calcStack,StackTree.__OperandTypesList(),count)
            logger.debug('First Element of Bracket or of all Calculation')
            if tokenresult[0]:
                weiredOperandsCounter += 1
            else:
                self.cmdParaMan.outdata += "<br>\nParsing Error: Expected Operand: Not Expected Token in Calcuation: "+str(restTypes[count])+" is of type "+str(type_)
                return False,tokenresult[1],tokenresult[2],weiredOperandsCounter
        elif weiredOperandsCounter == 0: # 0 when new op possible 1 when one operand before
            tokenresult = self._parseOneToken(parameterList[count+1],type_,calcStack,[LibCrygoldEVA.ParameterTypes.operationWithTwoOperands,LibCrygoldEVA.ParameterTypes.operationWithThreeOperands,LibCrygoldEVA.ParameterTypes.operationWithOneOperand],count)
            if tokenresult[0]:
                #print('aa '+str(calcStackOp.amountOperands(type_))+' '+str(type_))
                if type_ == LibCrygoldEVA.ParameterTypes.operationWithOneOperand:
                    operandsamount = 1
                elif type_ == LibCrygoldEVA.ParameterTypes.operationWithTwoOperands:
                    operandsamount = 2
                elif type_ == LibCrygoldEVA.ParameterTypes.operationWithThreeOperands:
                    operandsamount = 3
                weiredOperandsCounter = 1 - operandsamount # -1 when 2 operands
                # End of Operation is count = here plus amount Of Operands for
                # this Operation minus 1
            else:
                self.cmdParaMan.outdata += "<br>\nParsing Error: Expected Operation: Not Expected Token in Calcuation: "+str(restTypes[count])+" is of type "+str(type_)
                return False,tokenresult[1],tokenresult[2],weiredOperandsCounter
        else:
            self.cmdParaMan.outdata += "<br>\nParsing Error: Not Expected Token in Calcuation: "+str(restTypes[count])+" is of type "+str(type_)
            return False,tokenresult[1],tokenresult[2],weiredOperandsCounter
        self.cmdParaMan.outdata += "<br>\nPart Calculation Token parsed success= "+str(tokenresult[0])+"calc stack: "+str(calcStack)
        return tokenresult[0],tokenresult[1],tokenresult[2],weiredOperandsCounter

#        if type_ == LibCrygoldEVA.ParameterTypes.FileExistingOrReservedWord and count == 0 \
#        and self.__isOperator(restTypes[count+1]) \
#        and self.__isOperand(restTypes[count+2]):
#            firstCalcInBracket = True
#        elif count == 0 and restTypes[count] == LibCrygoldEVA.ParameterTypes.BracketOpen:
#            calcStack.append('()')
#            calcStack.append(0)
#            bracket = count
#            return True,restTypes,calcStack,bracket,weiredOperandsCounter
#        elif count > 0 and count + 1 < len(restTypes) and self.__isOperator(type_) \
#        and self.__isOperand(restTypes[count+1]):
#            firstCalcInBracket = False
#        else:
#            logger.debug('Things are not a calculation')
#            self.cmdParaMan.outdata += "<br>\nThings are not a calculation"
#            self.cmdParaMan.outdata += "<br>\nThey are: "+str(restTypes)
#            return False,restTypes,calcStack,bracket,weiredOperandsCounter
#
#        if firstCalcInBracket == True:
#            self.cmdParaMan.outdata += "<br>\nFirst Calculation"
#            calcStack.append(parameterList[count+1])
#            calcStack.append(self.cmdParaMan.getOneStepSeconds(parameterList[count+1]))
#            delta = 1
#        else:
#            delta = 0
#
#        op = OpTypesHandling.EnumKeyByStrKey(parameterList[count+1+delta])
#        if op is None:
#            self.cmdParaMan.outdata += "<br>\nOperation == None :" + str(parameterList[count+1+delta])
#            return False,restTypes,calcStack,bracket,weiredOperandsCounter
#        calcStack.append(op)
#
#        for amountMoreOperands in range(0,OpTypesHandling.calcStackOp.amountOperands(op)-2):
#            bracketsteps = 0
#            bracketopened = False
#            amountMoreOperandsB = amountMoreOperands + bracketsteps
#            if restTypes[count+1+delta+amountMoreOperandsB] == LibCrygoldEVA.ParameterTypes.BracketOpen:
#                calcStack.append('()')
#                bracket = count+1+delta+amountMoreOperandsB
#                bracketopened = True
#            if bracket is None:
#                # add 2nd 3rd etc operand:
#                calcStack.append(parameterList[count+2+delta+amountMoreOperandsB-bracketsteps])
#                # this is for clearify stepseconds number
#                if restTypes[count+1+delta+amountMoreOperandsB-bracketsteps] == LibCrygoldEVA.ParameterTypes.FlattenType:
#                    if self.__isCsvFileExisting(parameterList[count-delta-amountMoreOperandsB-bracketsteps]):
#                        calcStack.append(self.cmdParaMan.getOneStepSeconds(parameterList[count-delta-amountMoreOperandsB-bracketsteps]))
#                    else:
#                        calcStack.append(0)
#                else:
#                    calcStack.append(self.cmdParaMan.getOneStepSeconds(parameterList[count+2+delta+amountMoreOperandsB-bracketsteps]))
#            if restTypes[count+1+delta+amountMoreOperandsB] == LibCrygoldEVA.ParameterTypes.BracketClose:
#                bracketopened = False
#                bracketsteps += 1
#            if bracketopened:
#                bracketsteps += 1
#                # zählt hoch bei '(' 'einElement' ')' auf zahl 3,
#                # er wäre jetzt einen schritt weiter und muss nun aber 3 fach
#                # weiter gehen deshalb +3
#                # Ich muss hier später berücksichtigen dass ab operand 2 auch
#                # klammern ineinander sein können, was der code nicht
#                # berücksichtigt, wenn ein zweiter dritter operand eine klammer
#                # hat, berücksichtigt das hier nicht, pro operation mit ihren
#                # operanden
#                # Es funktioniert auch nicht, dass berücksichtigt wird wenn eine
#                # operation mit anzahlen von operanden: Also es funktioniert
#                # dass ein operand eine Klammer sei kann, aber vielleicht nicht,
#                # dass mehrere Operanden eine Klammer SIND
#
#                # Lösung, versucht einfach: Ich mache aus 2 nun 3
#                # Klassenfunktionen: statt pro Bracket und Operation:
#                # Fkt machen, die liste aus Brackets in Op gestaltet,
#                # Fkt, die das als Grundlage nutzt um einfacher pro Op zu parsen
#                # Fkt, die pro Bracket parseAll startet
#
#                # ParseAll ist pro Bracket
#                # ParseDetermineBracket ist bestimmen der Bracket
#                # _parseBringTokenToParseIt macht eine Op
#                # ich brauche festellen von mehreren Brackets pro Op
#
#                # Ablauf ist im Moment so, dass ParseAll jedes Token durch geht,
#                # wobei jedoch _parseBringTokenToParseIt macht, dass immer
#                # vor gesprungen wird je Op, und nach jeder Op wird bisher die
#                # letzte Bracket als ganzes Verstanden mit ihren Unterbrackets,
#                # aber ich möchte alle Brackets in einer Op einbeziehen
#
#                # Unterbrackets feststellen: macht schon die ParseDetermineBracket
#                # brauche ich aber auch um genau dieser selben Fkt mit zu geben
#                # und fest zu stellen, wenn es auf gleicher Ebene noch eine
#                # Bracket gibt, da beißt sich die Katze in den Schwanz!
#
#                # Jetzt stelle ich gerade fest, dass bei Bracket detektion mit
#                # return true die Operation frühzeitig beendet wird, dass das
#                # beahndelt werden kann, also wurde es doch schon richtig
#                # korrekt einprogrammiert
#
#                # Aber wie habe ich dann programmiert, dass weiter geparsed wird
#                # pro Bracket: weiredOperandsCounter geht erst hoch nach Ende des zweiten
#                # Operanden, so lange wird jedes Token untersucht und der
#                # Prozedur die pro Operation mit ihren Operanden durch geht,
#                # wird ohne jump einfach nur immer wieder das nächste Token mit
#                # gegeben aber auch die schleifenzählvariable, die alle token
#                # bestimmt als index des arrays der Parameter und der
#                # Parametertypen, dass die 2 arrays das array bestimmen der
#                # token der calc liste
#
#                # wenn pro entdeckter klammer die abarbeitung pro Op mit Opnds
#                # einfach mit True Okay abgebrochen wird, dann muss diese auch
#                # weiter gehen können, und zwar dann, immer wenn eine klammer
#                # pro Opnd behandelt wurde mit der BracketS Prozedur
#
#                # Ich brauche eine Prozedur pro Token, der die Situation kurz
#                # mitgegeben wird, und eine Prozedor pro ganze Op mit Opnds
#                # die Op die Pro Op mit Opnds ist, bricht immer mit True bei
#                # Klammer auf Fund ab, die neue Prozedur pro Token wird je ggf
#                # durch die Pro Op aufgerufen und eine Var stellt dann fest, ob
#                # ganze Op durch ist, eine var stellt fest wie viele token noch
#                # durch müssen bis für fkt die pro token ist, die var die sagt,
#                # dass alle token für op mit deren opnds durch ist, wird
#                # überprüft in der fkt die klammern behandelt
#
#                # der prozedur pro token muss mit gegeben werden: token, nr des
#                # tokens, was okay sein wird, was nicht okay sein wird, ggf was
#                # im zweifelsfall getan werden muss
#        #finished
#        weiredOperandsCounter+=1+delta+amountMoreOperands
#        self.cmdParaMan.outdata += "<br>\nPart Calculation Parameters Successful parsed "+str(calcStack)
#        return True,restTypes,calcStack,bracket,weiredOperandsCounter

    def _parseDetermineBracket(self,restTypes,parameterList,eldertree,elderResult,count,type_,tree1,innerBracketsCounter,bracketParameterList,bracketTypeList,bracket,weiredOperandsCounter,calcStack):
        self.cmdParaMan.outdata += "<br>\nParsing Loop Round "+str(count)+" Type:"+str(type_)
        #if bracket is None and count == 0:
        #   tree1[2].append([type_,count,[[],[]],tree1,eldertree,restTypes,parameterList,calcStack])
        #   eldertree[1].append(tree1)
        #if weiredOperandsCounter > 0:
        #    self.cmdParaMan.outdata += "<br>\nJump Count until 0: "+str(weiredOperandsCounter)
        #    weiredOperandsCounter -= 1
        #if weiredOperandsCounter:
        #    return True,parameterList,eldertree,elderResult,tree1,innerBracketsCounter,bracketParameterList,bracketTypeList,bracket,weiredOperandsCounter,calcStack
        if not bracket is None:
            self.cmdParaMan.outdata += "<br>\nIs Bracket"
            if innerBracketsCounter > 0 and type_ == LibCrygoldEVA.ParameterTypes.BracketClose:
                bracketTypeList.append(type_)
                bracketParameterList.append(parameterList[count+1])
                innerBracketsCounter -= 1
                self.cmdParaMan.outdata += "<br>\nOne More Bracket Closed"
                if count + 1 == len(restTypes):
                    self.cmdParaMan.outdata += "<br>\n"+str(innerBracketsCounter + 1)+" or more Brackets have to be closed!"
                    return False,parameterList,eldertree,elderResult,tree1,innerBracketsCounter,bracketParameterList,bracketTypeList,bracket,weiredOperandsCounter,calcStack
            elif innerBracketsCounter == 0 and type_ == LibCrygoldEVA.ParameterTypes.BracketClose:
                self.cmdParaMan.outdata += "<br>\nStart putting whole bracket to parse"
                #bracketParameterList.append(parameterList[count+1])
                if not self.__isBrackets(parameterList[bracket+1]+parameterList[count+1]):
                    self.cmdParaMan.outdata += "<br>\nEither not same kind of Brackets or not Brackets: "#+ str(len(parameterList))+' '+str(len(restTypes))
                    return False,parameterList,eldertree,elderResult,tree1,innerBracketsCounter,bracketParameterList,bracketTypeList,bracket,weiredOperandsCounter,calcStack
                self.cmdParaMan.outdata += "<br>\nParse what is in Bracket, ElderTree is None: "+str(tree1[0] is None)
                subResult = self._parseAll(bracketTypeList,bracketParameterList,tree1,elderResult)
                self.cmdParaMan.outdata += "<br>\nTree about Bracket got its Properties, ElderTree is None: "+str(tree1[0] is None)
                if subResult[0] == False:
                    self.cmdParaMan.outdata += "<br>\nParsing in Brackets failed"
                    return False,parameterList,eldertree,elderResult,tree1,innerBracketsCounter,bracketParameterList,bracketTypeList,bracket,weiredOperandsCounter,calcStack
                else:
                    self.cmdParaMan.outdata += "<br>\nParsing in Bracket went well"
                self.cmdParaMan.outdata += "<br>\nTypes in Bracket: "+ str(bracketTypeList)

                bracketTypeList = []
                bracketParameterList = [parameterList[0]]
                bracket = None
                self.cmdParaMan.outdata += "<br>\nBracket Closed, maybe after inner Brackets"
            elif type_ == LibCrygoldEVA.ParameterTypes.BracketOpen:
                bracketTypeList.append(type_)
                bracketParameterList.append(parameterList[count+1])
                innerBracketsCounter += 1
                self.cmdParaMan.outdata += "<br>\nOne More Bracket"
                if count + 1 == len(restTypes):
                    self.cmdParaMan.outdata += "<br>\n"+(innerBracketsCounter + 1)+" or more Brackets have to be closed!"
                    return False,parameterList,eldertree,elderResult,tree1,innerBracketsCounter,bracketParameterList,bracketTypeList,bracket,weiredOperandsCounter,calcStack

            elif type_ != LibCrygoldEVA.ParameterTypes.BracketOpen and type_ != LibCrygoldEVA.ParameterTypes.BracketClose:
                bracketTypeList.append(type_)
                bracketParameterList.append(parameterList[count+1])
                if count + 1 == len(restTypes):
                    self.cmdParaMan.outdata += "<br>\nOne or more Brackets have to be closed!"
                    return False,parameterList,eldertree,elderResult,tree1,innerBracketsCounter,bracketParameterList,bracketTypeList,bracket,weiredOperandsCounter,calcStack
            else:
                raise ValueError("Bracket if elif else structure Error")
            return True,parameterList,eldertree,elderResult,tree1,innerBracketsCounter,bracketParameterList,bracketTypeList,bracket,weiredOperandsCounter,calcStack

        if count + 1 == len(restTypes): # last For Loop Step
            if not bracket is None:
                self.cmdParaMan.outdata += "<br>\nLast bracket did not close"
                return False,parameterList,eldertree,elderResult,tree1,innerBracketsCounter,bracketParameterList,bracketTypeList,bracket,weiredOperandsCounter,calcStack
            if innerBracketsCounter != 0:
                if type_ == LibCrygoldEVA.ParameterTypes.BracketClose:
                    self.cmdParaMan.outdata += "<br>\nOne inner bracket closed, but not outer bracket"
                else:
                    self.cmdParaMan.outdata += "<br>\nClose bracket at ending!"
                return False,parameterList,eldertree,elderResult,tree1,innerBracketsCounter,bracketParameterList,bracketTypeList,bracket,weiredOperandsCounter,calcStack
        tokenSuccess,calcStack,bracket,weiredOperandsCounter = self._parseBringTokenToParseIt(restTypes,parameterList,calcStack,bracket,weiredOperandsCounter,count,type_ )
        if not tokenSuccess:
            return False,parameterList,eldertree,elderResult,tree1,innerBracketsCounter,bracketParameterList,bracketTypeList,bracket,weiredOperandsCounter,calcStack
        return True,parameterList,eldertree,elderResult,tree1,innerBracketsCounter,bracketParameterList,bracketTypeList,bracket,weiredOperandsCounter,calcStack

    def _parseAll(self,restTypes,parameterList,eldertree,elderResult):
        calcStack=[]
        if eldertree is None:
            tree1 = self.tree1
            tree1[2] = [restTypes,parameterList,calcStack,elderResult]
        else:
            tree1 = [eldertree,[],[restTypes,parameterList,calcStack,elderResult]] # 3 Elemente: Vater, Kinder, Eigenschaften
            eldertree[1].append(tree1)
            self.cmdParaMan.outdata += "<br>\nElder Tree Knows now about his children"
        if len(restTypes) == 1 and restTypes[0] == LibCrygoldEVA.ParameterTypes.FileExistingOrReservedWord:
                #print"only one "+str(parameterList)+' '+str(restTypes,))
            self.cmdParaMan.outdata += "<br>\nOnly one csv"
            #calcStack.append(op)
            if self.__isOperand(restTypes[0]) and len(parameterList) > 0:
                calcStack.append(parameterList[1])
                if os.path.isfile(parameterList[1]):
                    calcStack.append(self.cmdParaMan.getOneStepSeconds(parameterList[1]))
                else:
                    calcStack.append(0)
            return self._ParseTestPerBracket(calcStack,restTypes),calcStack,restTypes,tree1
        #if len(restTypes) == 2 or len(restTypes) == 0:
        #    self.cmdParaMan.outdata += "<br>\nUngood: RestTypes = 0 or 2"
        #    self.cmdParaMan.outdata += "<br>\nRestTypes = "+str(restTypes)
        #    return False,calcStack,restTypes,tree1
        if len(restTypes) > 1:
            ##print"blub"+str(restTypes))
            weiredOperandsCounter = -1
            bracket = None
            bracketTypeList = []
            bracketParameterList = [parameterList[0]]
            innerBracketsCounter = 0
            #print"set "+str([restTypes,parameterList,calcStack,elderResult]))
            tree1[2]=[restTypes,parameterList,calcStack,elderResult]
            #print(str(type(restTypes))+' ')
            for count, type_ in enumerate(restTypes):
                #print(str(type(parameterList))+' '+str(type(elderResult))+' '+str(type(eldertree))+' '+str(type(tree1))+' '+str(type(innerBracketsCounter)))
                EitherTokenOrBracketEndingSuccess,parameterList,eldertree,elderResult,tree1,innerBracketsCounter,bracketParameterList,bracketTypeList,bracket,weiredOperandsCounter,calcStack = self._parseDetermineBracket(restTypes,parameterList,eldertree,elderResult,count,type_,tree1,innerBracketsCounter,bracketParameterList,bracketTypeList,bracket,weiredOperandsCounter,calcStack)
                if not EitherTokenOrBracketEndingSuccess:
                    return False,calcStack,restTypes,tree1
            if weiredOperandsCounter != 0:
                self.cmdParaMan.outdata += "<br>\nParsing Failsure: "+str(-weiredOperandsCounter)+" Operands missing!"#+ str(len(parameterList))+' '+str(len(restTypes))
                return False,calcStack,restTypes,tree1
            return True,calcStack,restTypes,tree1
        else:
            self.cmdParaMan.outdata += "<br>\nIs Not a Operation with Operands"
        self.cmdParaMan.outdata += "<br>\nEnd of Parsing, Parsing failed"
        return False,calcStack,restTypes,tree1

    def _ParseTestPerBracket(self,calcStack,restTypes):
        self.cmdParaMan.outdata += "<br>\nParsing was okay"
        self.cmdParaMan.outdata += "<br>\nExecution began"
        combiCalcDone = False
        if calcStack!=[]:
            self.cmdParaMan.outdata += "<br>\nCalculation yes 1! CalcStackSize: "+str(len(calcStack))
            if len(calcStack)>4:
                self.cmdParaMan.outdata += "<br>\nCalculation yes 2!"
                if len(calcStack) >= 5 and (len(calcStack) - 5) % 3 == 0:
                    return True
                    #self.cmdParaMan.outdata += "<br>\nCalculation yes 3!"
                    #mulCharts = LibCrygoldEVA.ManyCalculations(calcStack,date1,date2,tree1)
                    #mulCharts.RestPartCalcListIntoStack().exec()
                    #self.cmdParaMan._out(mulCharts)
                    combiCalcDone = True
                    logger.debug("Calculations had been done 1!")
                else:
                    self.cmdParaMan.outdata += "<br>\nAmount of Parameters wrong!"
                    return False
        if not combiCalcDone:
            self.cmdParaMan.outdata += "<br>\nCalculations had not been done!"
            if restTypes[0] == LibCrygoldEVA.ParameterTypes.FileExistingOrReservedWord \
            or ( calcStack[0] == '()' and len(calcStack) == 2 ):
                return True
                #self.cmdParaMan.outdata += "<br>\nCalculation yes 3!"
                #mulCharts = LibCrygoldEVA.ManyCalculations(calcStack,date1,date2,tree1)
                #mulCharts.RestPartCalcListIntoStack().exec()
                #self.cmdParaMan._out(mulCharts)
                combiCalcDone = True
                #self.cmdParaMan.outdata += "<br>\njust output single chart!"
                #self.cmdParaMan.chartTimeLimited1 = LibCrygoldEVA.ChartDataTimeLimitedPlusTwoOutputs(parameterList[1],self.cmdParaMan.getOneStepSeconds(parameterList[1]),date1,date2).run()
#                    ThreeCharts.showChart(self.chartTimeLimited1.chartDisplayForNow,ThreeCharts)
#                    self.chartTimeLimited1.chartDisplayForNow()
                #self.cmdParaMan._out(self.cmdParaMan.chartTimeLimited1)
            else:
                self.cmdParaMan.outdata += "<br>\nFirst File is not a existing File!"
                return False
        else:
            logger.debug("Calculations had been done 2!")
            return False
        return False
