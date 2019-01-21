#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import operations
import csvMatch
import Stack


class Token():
    def __init__(self, OperandsContentHandlingOrOperation):
        self._token = OperandsContentHandlingOrOperation

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token):
        self._token = token

    def isTypeAsString(self):
        return str(type(self._token))

    def isOperandsContentHandling(self):
        if issubclass(type(self._token),csvMatch.OperandsContentHandling):
            return True
        else:
            return False

    def isOperateWhatEver(self):
        if type(self._token) is operations.IOperateWhatEver:
            return True
        else:
            return False

    def isOpTypesHandling(self):
        if type(self._token) is Stack.OpTypesHandling:
            return True
        else:
            return False

    def isNumber(self):
        if str(self._token).isnumeric():
            return True
        else:
            return False

    def isNumberOperation(self):
        if type(self._token) is operations.IOperator:
            return True
        else:
            return False


class Cursor():
    def __init__(self, graph):
        self._graph = graph
        self._x = 0
        self._y = 0
        # [[],[[][]],[],[[][][][]]]

    def setXY(self, x, y):
        self._x, self._y = x, y

    def getXY(self):
        return [self._x, self._y]

    def getLenY(self):
        return len(self._graph[self._x])

    def getLenX(self):
        return len(self._graph)

    @property
    def token(self):
        return self._graph[self._x][self._y]

    @token.setter
    def token(self, token):
        self._graph[self._x][self._y] = token
