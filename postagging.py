#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 16:30:31 2016-05-03

@author: heshenghuan (heshenghuan@sina.com)
http://github.com/heshenghuan
"""

import codecs
import math
import sys
import CharType

TAGSET = set()
TAGFREQ = {}
TRAN_PROB = {}
INIT_PROB = {}
OMIT_PROB = {}
ZERO_PROB = {}
CharTypeMap = CharType.CharType()

def readResource():
    print "Reading Character type information."
    CharTypeMap = CharType.CharType()
    CharTypeMap.initialize('./resource/')
    print "Reading Character type information OK.\n"


def readTagFile(TAGFILE='prob/ctb7_tags.txt'):
    TAGSET.clear()
    tag_input = codecs.open(TAGFILE, mode='r', encoding='utf8')
    is_first_line = True
    for line in tag_input.readlines():
        if is_first_line:
            is_first_line = False
            continue
        tag = line.strip()
        TAGSET.add(tag)
    print "\nLoad POS tag finished. Totally %d tags.\n" % len(TAGSET)
    tag_input.close()


def readTranProb(TRANPROBFILE='prob/ctb7_tranprob.txt'):
    TRAN_PROB.clear()
    print "Reading transition probability."
    infile = codecs.open(TRANPROBFILE, mode='r', encoding='utf8')
    is_first_line = True
    for line in infile.readlines():
        if is_first_line:
            is_first_line = False
            continue
        raw = line.strip().split()
        TRAN_PROB[raw[0]] = {}
        for i in range(1, len(raw)):
            tag, prob = raw[i].split(':')
            TRAN_PROB[raw[0]][tag] = float(prob)
    infile.close()
    print "Read Transition probability matrix OK.\n"


def readInitProb(INITPROBFILE='prob/ctb7_initprob.txt'):
    INIT_PROB.clear()
    print "Reading Start probability."
    infile = codecs.open(INITPROBFILE, mode='r', encoding='utf8')
    is_first_line = True
    for line in infile.readlines():
        if is_first_line:
            is_first_line = False
            continue
        raw = line.strip().split()
        INIT_PROB[raw[0]] = float(raw[1])
    infile.close()
    print "Read Start probability matrix OK.\n"


def readOmitProb(OMITPROBFILE='prob/ctb7_omit.txt', ZEROPROBFILE='prob/ctb7_zeroprob_katz.txt'):
    OMIT_PROB.clear()
    ZERO_PROB.clear()
    print "Reading Omission probability."
    infile = codecs.open(OMITPROBFILE, mode='r', encoding='utf8')
    is_first_line = True
    for line in infile.readlines():
        if is_first_line:
            is_first_line = False
            continue
        raw = line.strip().split()
        OMIT_PROB[raw[0]] = {}
        for i in range(1, len(raw)):
            tag, prob = raw[i].split(':')
            OMIT_PROB[raw[0]][tag] = float(prob)
    infile.close()

    zinfile = codecs.open(ZEROPROBFILE, mode='r', encoding='utf8')
    is_first_line = True
    for line in zinfile.readlines():
        if is_first_line:
            is_first_line = False
            continue
        raw = line.strip().split()
        ZERO_PROB[raw[0]] = float(raw[1])
    zinfile.close()
    print "Read Omission & zero probability matrix OK.\n"


def viterbiDecode(words):
    return 1

if __name__ == '__main__':
    readTagFile()
    readResource()
    readTranProb('prob/ctb7_tranprob.txt')
    readInitProb('prob/ctb7_initprob_katz.txt')
    readOmitProb()
