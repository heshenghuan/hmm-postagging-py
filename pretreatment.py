#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 17:11:38 2016-05-03

@author: heshenghuan (heshenghuan@sina.com)
http://github.com/heshenghuan
"""

import codecs
import sys

TAGSET = set()
TAGFREQ = {}
TRAN_PROB = {}
INIT_PROB = {}


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
    print "Load POS tag finished. Totally %d tags" % len(TAGSET)
    tag_input.close()


def getHmmModelInfo(CORPUSFILE='ctb7_update.txt'):
    readTagFile()
    if len(TAGSET) != 37:
        print len(TAGSET)
        print "Read POS tag file failed."
        sys.exit(0)

    for tag in TAGSET:
        INIT_PROB[tag] = 0
        TAGFREQ[tag] = 0
        TRAN_PROB[tag] = {}
        for next_tag in TAGSET:
            TRAN_PROB[tag][next_tag] = 0

    src_file = codecs.open(CORPUSFILE, mode='r', encoding='utf8')
    num = 0
    print "Reading corpus, building hmm parameters matrix",
    for line in src_file.readlines():
        raw_sent = line.strip().split()
        words = []
        tags = []
        for items in raw_sent:
            index = items.rfind('/')
            word = items[: index]
            tag = items[index + 1:]
            TAGFREQ[tag] += 1
            words.append(word)
            tags.append(tag)

        if len(words) != 0:
            INIT_PROB[tags[0]] += 1
            for i in range(len(tags) - 1):
                TRAN_PROB[tags[i]][tags[i + 1]] += 1

        num += 1
        if num % 100 == 0:
            print ".",
            if num % 2000 == 0:
                print "\t%d" % num
    print "Read corpus done."
    src_file.close()


def saveHMM(INIT_PROBFILE='ctb7_init.txt', TRAN_PROBFILE='ctb7_tran.txt',
            TAGFREQFILE='ctb7_tagFreq.txt'):
    i_out = codecs.open(INIT_PROBFILE, mode='w', encoding='utf8')
    t_out = codecs.open(TRAN_PROBFILE, mode='w', encoding='utf8')
    f_out = codecs.open(TAGFREQFILE, mode='w', encoding='utf8')

    print "Save HMM model."
    i_out.write("#INIT_PROB Frequency\n")
    for tag in TAGSET:
        i_out.write("%s %d\n" % (tag, INIT_PROB[tag]))

    t_out.write("#TRAN_PROB Frequency\n")
    for tag in TAGSET:
        t_out.write(tag + " ")
        for j in TRAN_PROB[tag].keys():
            t_out.write(j)
            t_out.write(":%d " % TRAN_PROB[tag][j])
        t_out.write("\n")

    f_out.write("#TAG_FREQUNCY Frequency\n")
    for tag in TAGSET:
        f_out.write("%s %d\n" % (tag, TAGFREQ[tag]))
    t_out.close()
    i_out.close()
    f_out.close()
    print "Finished."

if __name__ == '__main__':
    getHmmModelInfo()
    saveHMM()
