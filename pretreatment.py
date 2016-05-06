#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 17:11:38 2016-05-03

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


def calcInitProb(INIT_PROBFILE='ctb7_init.txt', smooth=0):
    i_input = codecs.open(INIT_PROBFILE, mode='r', encoding='utf8')
    i_out = codecs.open('ctb7_initprob.txt', mode='w', encoding='utf8')
    print "Calculate the start probability."
    is_first_line = True
    freq_sum = 0
    tag_freq = {}
    good_Turing_freq = {}
    for i in range(9):
        good_Turing_freq[i] = 0
    for line in i_input.readlines():
        if is_first_line:
            is_first_line = False
            continue
        raw = line.strip().split()
        num = int(raw[1])
        tag_freq[raw[0]] = num
        freq_sum += num
        if num <= 8:
            good_Turing_freq[num] += 1

    print good_Turing_freq
    print "Writing start log_probability to the file."
    i_out.write("#INIT_PROB log_probability\n")

    for tag in tag_freq.keys():
        i_out.write(tag + ' ')
        if smooth == 0:
            # No smoothing tech used
            if tag_freq[tag] == 0:
                i_out.write('-inf\n')
            else:
                freq = float(tag_freq[tag])
                i_out.write('%.4f\n' % (math.log(freq / freq_sum)))
        elif smooth == 1:
            # Laplace smoothing
            freq = tag_freq[tag]
            log_p = math.log((freq + 1.0) / (freq_sum + 37.0))
            i_out.write('%.4f\n' % log_p)
        elif smooth == 2:
            # Good-Turing smoothing
            break

# def calcLogProb(INIT_PROBFILE='ctb7_init.txt', TRAN_PROBFILE='ctb7_tran.txt',
#                 TAGFREQFILE='ctb7_tagFreq.txt', WORDFREQFILE='ctb7_words.txt'):
#     """
#     """
#     return

def curveFit(data):
    lnx = []
    lny = []
    for i in range(1, 9):
        if data[i] != 0:
            lnx.append(math.log(i))
            lny.append(math.log(data[i]))
    mean_x = sum(lnx)/len(lnx)
    mean_y = sum(lny)/len(lny)
    lxx = sum((x - mean_x)**2 for x in lnx)
    lxy = 0.0
    for i in range(len(lnx)):
        lxy += (lnx[i] - mean_x) * (lny[i] - mean_y)

    print "lnx:", lnx
    print "lny:", lny
    print "lxx:", lxx
    print "lxy:", lxy
    b1 = lxy / lxx
    b0 = mean_y - mean_x * b1
    print "b0: ", b0
    print "b1: ", b1
    return [math.exp(b0), b1]

if __name__ == '__main__':
    # getHmmModelInfo()
    # saveHMM()
    # calcInitProb(smooth=1)
    a = {0: 9, 1: 2, 2: 0, 3: 1, 4: 1, 5: 1, 6: 1, 7: 0, 8: 0}
    print a
    b = curveFit(a)
    a[2] = b[0] * math.pow(2, b[1])
    a[7] = b[0] * math.pow(7, b[1])
    a[8] = b[0] * math.pow(8, b[1])
    print a
