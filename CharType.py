#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 17:32:44 2016-05-12

@author: heshenghuan (heshenghuan@sina.com)
http://github.com/heshenghuan
"""

import codecs
import math
import sys


class CharType:

    def __init__(self):
        # 0:is not a punctuation 1: is a punctuation
        self.puncMap = {}

        # 0:ANum 1:CNum1, 2:CNum2, 3:English character, 4:date, 5:others;
        self.characterTypeMap = {}

        # Do not need these following type code now
        # # 0:frequency surname 1: common surname 2:given name
        # # 3:both 0+2 4:both 2+3 5:others
        # self.CNameMap = {}

        # # 0:not common foreign name character 1:common foreign name characte
        # self.FNameMap = {}

    def getPuncType(self, char):
        if self.puncMap.has_key(char):
            return 1
        else:
            return 0

    def getCharType(self, char):
        if self.characterTypeMap.has_key(char):
            return self.characterTypeMap[char]
        else:
            return 5

    def initialize(self, FOLDER='./resource/'):
        self.loadPunc(FOLDER + 'Punc')
        self.loadCharacterType(FOLDER)
        # loadCName(FOLDER)
        # loadFName(FOLDER + 'Punc')

    def loadPunc(self, FILE):
        self.puncMap.clear()
        infile = codecs.open(FILE, mode='r', encoding='utf8')
        num = 1
        for line in infile.readlines():
            if num == 1 or num == 2:
                num += 1
                continue
            else:
                raw = line.strip()
                self.puncMap[raw] = 1
                num += 1
        infile.close()

    def loadCharacterType(self, FOLDER):
        self.characterTypeMap.clear()
        # Read Arabic number
        ANum = codecs.open(FOLDER + 'ANum', mode='r', encoding='utf8')
        num = 1
        for line in ANum.readlines():
            if num == 1 or num == 2:
                num += 1
                continue
            else:
                raw = line.strip()
                self.characterTypeMap[raw] = 0
                num += 1
        ANum.close()
        # Read Chinese Number character
        CNum1 = codecs.open(FOLDER + 'CNum1', mode='r', encoding='utf8')
        num = 1
        for line in CNum1.readlines():
            if num == 1 or num == 2:
                num += 1
                continue
            else:
                raw = line.strip()
                self.characterTypeMap[raw] = 1
                num += 1
        CNum1.close()

        CNum2 = codecs.open(FOLDER + 'CNum2', mode='r', encoding='utf8')
        num = 1
        for line in CNum2.readlines():
            if num == 1 or num == 2:
                num += 1
                continue
            else:
                raw = line.strip()
                self.characterTypeMap[raw] = 2
                num += 1
        CNum2.close()

        # Read English character
        EChar = codecs.open(FOLDER + 'EChar', mode='r', encoding='utf8')
        num = 1
        for line in EChar.readlines():
            if num == 1 or num == 2:
                num += 1
                continue
            else:
                raw = line.strip()
                self.characterTypeMap[raw] = 3
                num += 1
        EChar.close()
        # Read date character
        Date = codecs.open(FOLDER + 'Date', mode='r', encoding='utf8')
        for line in Date.readlines():
            if num == 1 or num == 2:
                num += 1
                continue
            else:
                raw = line.strip()
                self.characterTypeMap[raw] = 4
                num += 1
        Date.close()
