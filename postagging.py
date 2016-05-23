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
ZERO = math.log(1e-7)  # this value liked to be adjust more


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
    T = len(words)
    prb, prb_max = 0., 0.
    toward = []
    back = []

    for i in range(T):
        toward.append({})
        back.append({})
        for j in TAGSET:
            toward[i][j] = float('-inf')
            back[i][j] = ' '

    # run viterbi
    # print words[0]
    omit_prob = getOmitProb(words[0])
    # print omit_prob
    for s in TAGSET:
        toward[0][s] = INIT_PROB[s] + omit_prob[s]
        back[0][s] = 'end'
    # toward algorithm
    for t in range(1, T):
        omit_prob = getOmitProb(words[t])
        # print omit_prob
        for s in TAGSET:
            prb = float('-inf')
            prb_max = float('-inf')
            state_max = 'NN'
            for i in TAGSET:
                prb = toward[t - 1][i] + TRAN_PROB[i][s] + omit_prob[s]
                if prb > prb_max:
                    prb_max = prb
                    state_max = i
            toward[t][s] = prb_max
            back[t][s] = state_max
            # print prb_max, state_max
    # backward algorithm to get the best tag sequence
    index = T - 1
    taglist = []
    prb_max = float('-inf')
    state_max = ''
    for s in TAGSET:
        prb = toward[T - 1][s]
        # print s, prb
        if prb > prb_max:
            prb_max = prb
            state_max = s
    taglist.append(state_max)
    while index >= 1:
        pre_state = back[index][taglist[0]]
        taglist.insert(0, pre_state)
        index -= 1
    return taglist


def getOmitProb(word):
    prb = {}
    for s in TAGSET:
        prb[s] = ZERO
    if OMIT_PROB.has_key(word):
        for key in OMIT_PROB[word].keys():
            prb[key] = OMIT_PROB[word][key]
    else:
        if len(word) == 1:
            if CharTypeMap.getPuncType(word) == 1:
                prb['PU'] = 0.0
            else:
                typ = CharTypeMap.getCharType(word)
                if typ == 0 or typ == 1 or typ == 2:
                    prb['CN'] = 0.0
                elif typ == 4:
                    prb['NT'] = -3.9979
                else:
                    prb = ZERO_PROB
        else:
            prb = ZERO_PROB
    return prb


def posTagFile(FILE, OUTFILE):
    infile = codecs.open(FILE, mode='r', encoding='utf8')
    outfile = codecs.open(OUTFILE, mode='w', encoding='utf8')
    num = 0
    for line in infile.readlines():
        raw = line.strip()
        num += 1
        if num % 100 == 0:
            print '.',
            if num % 1000 == 0:
                print '\t%d sentences.' % num
        if raw == "":
            outfile.write('\n')
            continue
        words = raw.split()
        tags = posTagSent(words)
        for i in range(len(words)):
            outfile.write(words[i] + '/' + tags[i] + ' ')
        outfile.write('\n')
    print "POS tagging finished. Totally %d lines." % num
    infile.close()
    outfile.close()


def posTagSent(words):
    return viterbiDecode(words)

if __name__ == '__main__':
    readTagFile()
    readResource()
    readTranProb('prob/ctb7_tranprob.txt')
    readInitProb('prob/ctb7_initprob_katz.txt')
    readOmitProb()
    posTagFile(sys.argv[1], sys.argv[2])
