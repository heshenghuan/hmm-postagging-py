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

TAGSET = set()
TAGFREQ = {}
TRAN_PROB = {}
INIT_PROB = {}
OMIT_PROB = {}
ZERO_PROB = {}


def readTagFile(TAGFILE='ctb7_tags.txt'):
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


def readTranProb(TRANPROBFILE='ctb7_tranprob.txt'):
    TRAN_PROB.clear()
    print "\nReading transition probability."
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


def readInitProb(INITPROBFILE='ctb7_initprob.txt'):
    INIT_PROB.clear()
    print "\nReading Start probability."
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


def readOmitProb(OMITPROBFILE='ctb7_omit.txt', ZEROPROBFILE='ctb7_zeroprob_katz.txt'):
    OMIT_PROB.clear()
    ZERO_PROB.clear()
    print "\nReading Omission probability."
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

if __name__ == '__main__':
    readTagFile()
    readTranProb('ctb7_tranprob.txt')
    readInitProb('ctb7_initprob_katz.txt')
    readOmitProb()
