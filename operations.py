#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import math
import csvMatch
#import LibCrygoldEVA
#from LibCrygoldEVA import calcStackOp as OpEnum
import CursorNToken
import logging
import chartdata2less
import numpy
from enum import IntEnum
import copy
logger = logging.getLogger('PyCryGold')
logger.setLevel(logging.DEBUG)

class IOperateWhatEver():
    def __init__(self):
        self.tokens = []
        self.result = None
    @abstractmethod
    def execute(self):
        pass
    @abstractmethod
    def addOperand(self,token):
        logger.debug('add Operand '+str(token))
        self.tokens.append(token)
    @abstractmethod
    def LenOperands(self):
        return len(self.tokens)
    @abstractmethod
    def getResult(self):
        return self.result

class IOperateCharts(IOperateWhatEver):
    tokens=[]
    def __init__(self):
        super().__init__()
        self.parameter=[]

class INumberOperator(IOperateWhatEver):
    tokens=[]
    def __init__(self):
        self.tokens=[]
        self.parameter=[]
        self.result = None
    @abstractmethod
    def addToken(self,token):
        self.tokens.append(token)
        return self

#class IOpStatistics(IOperateCharts):
#    pass
#
#class OpMedian(IOpStatistics):
#    def execute(self):
#        result=[]
#        for m in self.matrices:
#            m = m.sort()
#            self.result.append(m[int(len(self.tokens) / 2)])
#
#class OpAverage(IOpStatistics):
#    def execute(self):
#        self.result = []
#        for a in self.matrices:
#            self.result.append([])
#            for b in a:
#                self.result[-1] += a
#            self.result[-1] = self.result[-1] / len(a)
#        return self
#class OpMaximum(IOpStatistics):
#    def execute(self):
#        self.result = []
#        for a in self.matrices:
#            self.result.append([])
#            self.result[-1] = self.matrices.sort()
#            self.result[-1] = self.result[-1][len(self.tokens) -1]
#        return self
#class OpMinimum(IOpStatistics):
#    def execute(self):
#        self.result = []
#        for a in self.matrices:
#            self.result.append([])
#            self.result[-1] = self.matrices.sort()
#            self.result[-1] = self.result[-1][0]
#        return self
#
##Streuung
#class OpDispersion(IOpStatistics):
#    def execute(self):
#        avg = OpAverage()
#        avg.matrices = self.matrices
#        avg = avg.execute().result()
#        a = 0
#        dispN = []
#        for b in self.matrices:
#            dispN.append([])
#            for oneAvg in avg:
#                dispN[-1] += b - oneAvg
#            dispN[-1] /= len(b)
#        self.result = a # math.sqrt(a)
#class OpVariance(OpDispersion):
#    def execute(self):
#        for resN in self.result:
#            resN = math.sqrt(resN)
#
## Entspricht wohl Durchschnitt
#class OpExpectedValue(OpAverage):
#    pass
#
#class OpCovariance(IOpMultipleTokenLists):
#    def execute(self):
#        super().setAmountTokenLists(2)
#    # COV(X,Y) = E[(X-E(X))*(Y-E(Y))]
#
#class OpCorrelation(IOpStatistics):
#            pass



#a = OpAdd()
#a= a.addToken(2).addToken(3).execute().getResult()
#print(str(a))
#a = OpMul()
#a= a.addToken(2).addToken(3).execute().getResult()
#print(str(a))
#a = OpDiv()
#a= a.addToken(2).addToken(3).addToken(0).execute().getResult()
#print(str(a))


#class joinAnyHow(csvMatch.join2CSVs):
#    def __init__(self,chartfilename1,chartfilename2,operation,diffseconds2,new1name="None",new2name="None"):
#        super().__init__(chartfilename1,chartfilename2,operation,diffseconds2,new1name,new2name)

#class OpMul(IOperateCharts):
#    def __init__(self):
#        super().__init__()
#    def execute(self):
#        join = joinMul(self.tokens[1].token,self.tokens[0].token)
#        self.result = CursorNToken.Token(join.toChartObjects()[0])
#        return self
##calcStackOp.div
class OpAll(IOperateCharts):
    def __init__(self,typesHandling,operation):
        super().__init__()
        self.operation = operation
        self.typesHandling = typesHandling
    def execute(self):
        join = joinOp(self.tokens[1].token,self.tokens[0].token,self.operation,self.typesHandling)
        self.result = CursorNToken.Token(join.toChartObjects()[0])
        return self

#class OpDiv(IOperateCharts):
#    def __init__(self):
#        super().__init__()
#    def execute(self):
#        join = joinDiv(self.tokens[1].token,self.tokens[0].token)
#        self.result = CursorNToken.Token(join.toChartObjects()[0])
#        return self
#
#class OpAdd(IOperateCharts):
#    def __init__(self):
#        super().__init__()
#    def execute(self):
#        join = joinAdd(self.tokens[1].token,self.tokens[0].token)
#        self.result = CursorNToken.Token(join.toChartObjects()[0])
#        return self

#class OpLog(IOperateCharts):
#    def __init__(self):
#        super().__init__()
#    def execute(self):
#        join = joinLog(self.tokens[1].token,self.tokens[0].token)
#        self.result = CursorNToken.Token(join.toChartObjects()[0])
#        return self
#%s/chartdata2less\.calcOps/chartdata2less.ReduceDataToFourThings.calcOps/g
class OpDiffuse(IOperateWhatEver):
    def __init__(self,every,allOperations,typesHandling,once=False):
        self.every = every
        self.allOperations = allOperations
        self.typesHandling = typesHandling
        self.once = once
        super().__init__()
    def execute(self):
        if type(self.tokens[0].token) is float:
            self.tokens[0].token = int(self.tokens[0].token)
        lastLetter = str(str(self.tokens[0].token)[-1])
        from LibCrygoldEVA import CommandParameterManaging as main
        if lastLetter.isnumeric() and not lastLetter.isalpha():
            self.tokens[0].token = str(self.tokens[0].token)+'d'
        elif not main.isFlattenType(self.tokens[0].token):
            raise ValueError('Parameter is not Flatten Type')
        diffuse = chartdata2less.ReduceDataToFourThings(self.tokens[1].token,self.tokens[0].token,self.every,self.allOperations,self.once)
        #self.result = CursorNToken.Token(csvMatch.OperandsContentHandling(self.tokens[1].token.getOneStepSeconds(),numpy.transpose(diffuse.out(),(1, 0)),'','',''))
        try:
            diffusefloat = float(diffuse.out()[0])
        except:
            diffusefloat = None
            pass
        if type(diffuse) is chartdata2less.ReduceDataToFourThings and not type(diffusefloat) is float:
            self.result = CursorNToken.Token(csvMatch.OperandsContentHandling(self.tokens[1].token.getOneStepSeconds(),diffuse.out(),'','',''))
        elif type(diffusefloat) is float:
            #print(str((diffuse.out()[1])))
            self.result = CursorNToken.Token(diffuse.out())
        else:
            print(str(type(diffuse)))
            raise ValueError("Neither float nor chartdata2less.ReduceDataToFourThings")
        return self

#class joinMul(csvMatch.join2CSVs,INumberOperator):
#    def __init__(self,OperandsContentHandling1,OperandsContentHandling2):
#        super().__init__(OperandsContentHandling1.toPyStdStructure(),OperandsContentHandling2.toPyStdStructure(),calcStackOp.mul,OperandsContentHandling2.getOneStepSeconds(),"None","None")
#
class joinOp(csvMatch.join2CSVs,INumberOperator):
    def __init__(self,OperandsContentHandling1,operand2,operation,typesHandling):
        self.operation = operation
        #print(str(type(operation)))
        #raise ""
        if issubclass(type(operand2),csvMatch.OperandsContentHandling):
            opsec = operand2.getOneStepSeconds()
            operand2 = operand2.toPyStdStructure()
            if issubclass(type(OperandsContentHandling1),csvMatch.OperandsContentHandling):
                operand1 = OperandsContentHandling1.toPyStdStructure()
            else:
                operand1 = OperandsContentHandling1
        elif issubclass(type(OperandsContentHandling1),csvMatch.OperandsContentHandling):
            opsec = OperandsContentHandling1.getOneStepSeconds()
            if issubclass(type(OperandsContentHandling1),csvMatch.OperandsContentHandling):
                operand1 = OperandsContentHandling1.toPyStdStructure()
            else:
                operand1 = OperandsContentHandling1
        else:
            opsec = 0
            operand1 = OperandsContentHandling1
        super().__init__(operand1,operand2,operation,opsec,typesHandling)

#class joinDiv(csvMatch.join2CSVs,INumberOperator):
#    def __init__(self,OperandsContentHandling1,op2):
#        if type(op2) is csvMatch.OperandsContentHandling:
#            ops = op2.getOneStepSeconds()
#            op2 = op2.toPyStdStructure()
#        else:
#            ops = OperandsContentHandling1.getOneStepSeconds()
#        super().__init__(OperandsContentHandling1.toPyStdStructure(),op2,calcStackOp.div,ops,"None","None")
#
#class joinAdd(csvMatch.join2CSVs,INumberOperator):
#    def __init__(self,OperandsContentHandling1,OperandsContentHandling2):
#        super().__init__(OperandsContentHandling1.toPyStdStructure(),OperandsContentHandling2.toPyStdStructure(),calcStackOp.add,OperandsContentHandling2.getOneStepSeconds(),"None","None")
#
#class joinLog(csvMatch.join2CSVs,INumberOperator):
#    def __init__(self,OperandsContentHandling1,logbase):
#        super().__init__(OperandsContentHandling1.toPyStdStructure(),logbase,calcStackOp.loga,OperandsContentHandling1.getOneStepSeconds(),"None","None")

class calcStackOp(IntEnum):
    def amountOperands(op):
        if op <= 19 and op > 0:
            return 2
        elif op in range(20,25):
            return 3
        elif op in [25,26]:
            return 1
        else:
            raise ValueError("Operation Unknown")
    mul = 1
    div = 2
    add = 3
    loga = 4
    diffuse = 5
    sub = 6
    pow = 7
    root = 8
    diffuse2 = 9
    min = 10
    max = 11
    med = 12
    avg = 13
    aswell = 14
    begin = 15
    end = 16
    variance = 17
    standarddeviation = 18
    quantileOfAll = 19
    quantileMoving = 20
    quantileSteps = 21
    correlationOfAll = 22
    correlationMoving = 23
    correlationStepps = 24
    negative = 25
    same = 26

class OpTypesHandling():
    def __init__(self,type_):
        if type(type_) is calcStackOp:
            self.type = type_
        elif type(type_) is str:
            self.type = OpTypesHandling.EnumKeyByStrKey(type_)
        else:
            raise ValueError("not str nor enum")
        if self.type is None:
            raise ValueError("type must not be none")
#        self.options = { calcStackOp.mul : OpAll, \
#        calcStackOp.div : OpAll, \
#        calcStackOp.add : OpAll, \
#        calcStackOp.loga : OpAll, \
#        calcStackOp.sub : OpAll, \
#        calcStackOp.pow : OpAll, \
#        calcStackOp.root : OpAll, \
#        calcStackOp.aswell : OpAll, \
#        calcStackOp.diffuse : OpDiffuse, \
#        calcStackOp.max : OpDiffuse, \
#        calcStackOp.min : OpDiffuse, \
#        calcStackOp.avg : OpDiffuse, \
#        calcStackOp.med : OpDiffuse, \
#        calcStackOp.diffuse2 : OpDiffuse }
        self.opsMapByEnum = copy.deepcopy(OpTypesHandling.OpFromEnum)
        self.Map4thisOp = self.opsMapByEnum[type_]
        self.Map4thisOp['OpObjParameter'].append(self)
        if self.Map4thisOp['OpObj'] is OpAll:
            self.Map4thisOp['OpObjParameter'].append(self.type)
        if type_ == calcStackOp.begin:
            self.Map4thisOp['OpObjParameter'].append(True) # Once True bei Begin
        #if type_ == calcStackOp.quantileMoving:
        #    self.Map4thisOp['OpObjParameter'].append(quantile)


    Ops = [ { 'calc' : csvMatch.join2CSVs._mul, 'OpObj' : OpAll, 'OpObjParameter' : []} ,\
            { 'calc' : csvMatch.join2CSVs._div, 'OpObj' : OpAll, 'OpObjParameter' : []} , \
            { 'calc' : csvMatch.join2CSVs._add, 'OpObj' : OpAll, 'OpObjParameter' : [] } , \
            { 'calc' : csvMatch.join2CSVs._log, 'OpObj' : OpAll, 'OpObjParameter' : [] } , \
            { 'calc' : None, 'OpObj' : OpDiffuse, 'OpObjParameter' : [False,[chartdata2less.ReduceDataToFourThings.calcOps.AVERAGE,chartdata2less.ReduceDataToFourThings.calcOps.MIN,chartdata2less.ReduceDataToFourThings.calcOps.MAX,chartdata2less.ReduceDataToFourThings.calcOps.MEDIAN]] } , \
            { 'calc' : None, 'OpObj' : OpDiffuse, 'OpObjParameter' : [False,[chartdata2less.ReduceDataToFourThings.calcOps.MAX]]} , \
            { 'calc' : None, 'OpObj' : OpDiffuse, 'OpObjParameter' : [False,[chartdata2less.ReduceDataToFourThings.calcOps.MIN]]} , \
            { 'calc' : None, 'OpObj' : OpDiffuse, 'OpObjParameter' : [True,[chartdata2less.ReduceDataToFourThings.calcOps.MEDIAN]]} , \
            { 'calc' : None, 'OpObj' : OpDiffuse, 'OpObjParameter' : [True,[chartdata2less.ReduceDataToFourThings.calcOps.AVERAGE]]} , \
            { 'calc' : None, 'OpObj' : OpDiffuse, 'OpObjParameter' : [True,[chartdata2less.ReduceDataToFourThings.calcOps.AVERAGE,chartdata2less.ReduceDataToFourThings.calcOps.MIN,chartdata2less.ReduceDataToFourThings.calcOps.MAX,chartdata2less.ReduceDataToFourThings.calcOps.MEDIAN]] } , \
            { 'calc' : csvMatch.join2CSVs._pow, 'OpObj' : OpAll, 'OpObjParameter' : [] } , \
            { 'calc' : csvMatch.join2CSVs._aswell, 'OpObj' : OpAll, 'OpObjParameter' : [] } , \
            { 'calc' : csvMatch.join2CSVs._root, 'OpObj' : OpAll, 'OpObjParameter' : [] }, \
            { 'calc' : csvMatch.join2CSVs._sub, 'OpObj' : OpAll, 'OpObjParameter' : [] }, \
            { 'calc' : None, 'OpObj' : OpDiffuse, 'OpObjParameter' : [False,[chartdata2less.ReduceDataToFourThings.calcOps.BEGIN]]}, \
            { 'calc' : None, 'OpObj' : OpDiffuse, 'OpObjParameter' : [False,[chartdata2less.ReduceDataToFourThings.calcOps.END]]}, \
            { 'calc' : None, 'OpObj' : OpDiffuse, 'OpObjParameter' : [True,[chartdata2less.ReduceDataToFourThings.calcOps.VARIANCE]]}, \
            { 'calc' : None, 'OpObj' : OpDiffuse, 'OpObjParameter' : [True,[chartdata2less.ReduceDataToFourThings.calcOps.STANDARDDEVIATION]]}, \
            { 'calc' : None, 'OpObj' : OpAll, 'OpObjParameter' : [] }, \
            { 'calc' : None, 'OpObj' : OpDiffuse, 'OpObjParameter' : [True,[chartdata2less.ReduceDataToFourThings.calcOps.QUANTILE]]}, \
            { 'calc' : None, 'OpObj' : OpDiffuse, 'OpObjParameter' : [False,[chartdata2less.ReduceDataToFourThings.calcOps.QUANTILE]]}, \
            { 'calc' : None, 'OpObj' : OpAll, 'OpObjParameter' : [] }, \
            { 'calc' : None, 'OpObj' : OpDiffuse, 'OpObjParameter' : [True,[chartdata2less.ReduceDataToFourThings.calcOps.QUANTILE]]}, \
            { 'calc' : None, 'OpObj' : OpDiffuse, 'OpObjParameter' : [False,[chartdata2less.ReduceDataToFourThings.calcOps.QUANTILE]]}, \
            { 'calc' : csvMatch.join2CSVs._mul, 'OpObj' : OpAll, 'OpObjParameter' : [] }, \
            { 'calc' : csvMatch.join2CSVs._aswell, 'OpObj' : OpAll, 'OpObjParameter' : [] }]

    OpFromString = { 'mul' : Ops[0], \
                           'div' : Ops[1], \
                           'add' : Ops[2], \
                           'log' : Ops[3], \
                           'diffuse' : Ops[4], \
                           'max' : Ops[5], \
                           'min' : Ops[6], \
                           'med' : Ops[7], \
                           'avg' : Ops[8], \
                           'diffuse2' : Ops[9], \
                           'pow' : Ops[10], \
                           'aswell' : Ops[11], \
                           'root' : Ops[12], \
                           'sub' :Ops[13], \
                           'begin' :Ops[14], \
                           'end' : Ops[15], \
                           'vari' : Ops[16], \
                           'stddevi' : Ops[17], \
                           'quantileAll' : Ops[18], \
                           'quantileMoving' : Ops[19], \
                           'quantileSteps' : Ops[20], \
                           'correlationAll' : Ops[21], \
                           'correlationMoving' : Ops[22], \
                           'correlationSteps' : Ops[23], \
                           'negative' : Ops[24], \
                           'same' : Ops[25] }

    OpFromEnum = { calcStackOp.mul : Ops[0], \
                           calcStackOp.div : Ops[1], \
                           calcStackOp.add : Ops[2], \
                           calcStackOp.loga : Ops[3], \
                           calcStackOp.diffuse : Ops[4], \
                           calcStackOp.max : Ops[5], \
                           calcStackOp.min : Ops[6], \
                           calcStackOp.med : Ops[7], \
                           calcStackOp.avg : Ops[8], \
                           calcStackOp.diffuse2 : Ops[9], \
                           calcStackOp.pow : Ops[10], \
                           calcStackOp.aswell : Ops[11], \
                           calcStackOp.root : Ops[12], \
                           calcStackOp.sub :Ops[13], \
                           calcStackOp.begin :Ops[14], \
                           calcStackOp.end :Ops[15], \
                           calcStackOp.variance :Ops[16], \
                           calcStackOp.standarddeviation :Ops[17], \
                           calcStackOp.quantileOfAll :Ops[18], \
                           calcStackOp.quantileMoving :Ops[19], \
                           calcStackOp.quantileSteps :Ops[20], \
                           calcStackOp.correlationOfAll :Ops[21], \
                           calcStackOp.correlationMoving :Ops[22], \
                           calcStackOp.correlationStepps :Ops[23], \
                           calcStackOp.negative :Ops[24], \
                           calcStackOp.same :Ops[25] }

    @staticmethod
    def EnumKeyByStrKey(text):
        index = list(OpTypesHandling.OpFromString.keys()).index(text)
        return list(OpTypesHandling.OpFromEnum.keys())[index]

    @staticmethod
    def StrKeyByEnumKey(enum):
        index = list(OpTypesHandling.OpFromEnum.keys()).index(enum)
        return list(OpTypesHandling.OpFromString.keys())[index]

    def getCalcDelegat(self):
        return self.Map4thisOp['calc']

    def execOpMethod(self):
        return self.Map4thisOp['OpObj'](*self.Map4thisOp['OpObjParameter'])
#        if not self.options[self.type] is OpDiffuse:
#            return self.options[self.type](self.type)
#        elif self.type in [calcStackOp.diffuse, \
#                           calcStackOp.max, \
#                           calcStackOp.min]:
#            if self.type is calcStackOp.max:
#                return self.options[self.type](False,[chartdata2less.ReduceDataToFourThings.calcOps.MAX])
#            elif self.type is calcStackOp.min:
#                return self.options[self.type](False,[chartdata2less.ReduceDataToFourThings.calcOps.MIN])
#            else:
#                return self.options[self.type](False)

    #allOperations=[calcOps.AVERAGE,calcOps.MIN,calcOps.MAX,calcOps.MEDIAN]
#        elif self.type in [calcStackOp.diffuse2, \
#                           calcStackOp.avg ,\
#                           calcStackOp.med]:
#            if self.type is calcStackOp.avg:
#                return self.options[self.type](True,[chartdata2less.ReduceDataToFourThings.calcOps.AVERAGE])
#            elif self.type is calcStackOp.med:
#                return self.options[self.type](True,[chartdata2less.ReduceDataToFourThings.calcOps.MEDIAN])
#            else:
#                return self.options[self.type](True)
#    @staticmethod
#    def getOperationList():
#        return list(OpTypesHandling.staticOpMap.keys())
        #return ['mul','div','add','log','diffuse','sub','pow','root','diffuse2','max','min','med','avg','aswell']
    @staticmethod
    def isAnOperation(op):
        #print("ABCDEFG "+str(op)+" "+str(list(OpTypesHandling.OpFromString.keys())))
        if op in OpTypesHandling.OpFromString.keys():
            return True
        if type(op) is calcStackOp:
            return True
        return False
#    @staticmethod
#i    def getEnumFromString(text):
#        return next(iter(OpTypesHandling.staticOpMap[text]))
#        opnamestr={     'mul' : calcStackOp.mul, \
#                        'div' : calcStackOp.div, \
#                        'add' : calcStackOp.add, \
#                        'log' : calcStackOp.loga, \
#                        'diffuse' : calcStackOp.diffuse, \
#                        'max' : calcStackOp.max, \
#                        'min' : calcStackOp.min , \
#                        'med' : calcStackOp.med, \
#                        'avg' : calcStackOp.avg, \
#                        'diffuse2' : calcStackOp.diffuse2, \
#                        'pow' : calcStackOp.pow, \
#                        'aswell' : calcStackOp.aswell, \
#                        'root' : calcStackOp.root, \
#                        'sub' : calcStackOp.sub }
#        if not OpTypesHandling.isAnOperation(text):
#            return None
#        else:
#            return opnamestr[text]



