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


def readTagFreq(TAGFREQFILE='ctb7_tagFreq.txt', T=10):
    tag_freq = {}
    N = {}
    for i in range(T + 1):
        N[i] = 0.
    infile = codecs.open(TAGFREQFILE, mode='r', encoding='utf8')
    is_first_line = True
    for line in infile.readlines():
        if is_first_line:
            is_first_line = False
            continue
        raw = line.strip().split()
        tag_freq[raw[0]] = int(raw[1])
        if int(raw[1]) <= T:
            N[int(raw[1])] += 1
    infile.close()
    return tag_freq, N


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


def saveFreqency(INIT_PROBFILE='ctb7_init.txt', TRAN_PROBFILE='ctb7_tran.txt', TAGFREQFILE='ctb7_tagFreq.txt'):
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


def calcOmitProb(TAGFREQFILE='ctb7_tagFreq.txt', WORDFILE='ctb7_words.txt', smooth=0, T=10):
    tag_freq, N = readTagFreq(TAGFREQFILE)
    infile = codecs.open(WORDFILE, mode='r', encoding='utf8')
    omitfile = codecs.open('ctb7_omit.txt', mode='w', encoding='utf8')
    omitfile.write("#Omit probability\n")
    words = {}
    is_first_line = True
    for line in infile.readlines():
        if is_first_line:
            is_first_line = False
            continue
        raw = line.strip().split()
        w = raw[0]
        words[w] = {}
        for i in range(1, len(raw)):
            item = raw[i].split(":")
            tag = item[0]
            num = int(item[1])
            words[w][tag] = num

    zeroProbFile = codecs.open('ctb7_zeroprob.txt', mode='w', encoding='utf8')
    zeroProbFile.write("#Zero probability for each tag\n")
    tagsum = sum(tag_freq[k] for k in tag_freq.keys())
    if smooth == 2:
        curveTag = sum(1 if N[i] != 0 else 0 for i in range(1, T + 1))
        if curveTag > 1:
            theta = curveFit(N, T)
            # print theta
            dr = KatzGoodTuring(theta, N, T)
            # print dr
        else:
            dr = [1e-6 * tag_freq[tag]]
            for i in range(1, T):
                dr.append(float(i))
    for tag in TAGSET:
        freq = tag_freq[tag]
        if smooth == 0:
            p = math.log(freq * 1.0 / tagsum)
            zeroProbFile.write(tag + " %.4f\n" % p)
        elif smooth == 1:
            p = math.log((freq + 1.0) / (tagsum + 37.0))
            zeroProbFile.write(tag + " %.4f\n" % p)
        elif smooth == 2:
            if freq < T:
                p = math.log((dr[freq]) / tagsum)
            else:
                p = math.log(freq * 1.0 / tagsum)
            zeroProbFile.write(tag + " %.4f\n" % p)
    zeroProbFile.close()

    # write omit
    for w in words.keys():
        omitfile.write(w + ' ')
        for tag in words[w].keys():
            num = words[w][tag]
            if smooth == 0:
                omitfile.write(tag)
                omitfile.write(':%.4f ' %
                               (math.log(num * 1.0 / tag_freq[tag])))
            elif smooth == 1:
                # Laplace smoothing
                log_p = math.log((num + 1.0) / (tag_freq[tag] + 37.0))
                omitfile.write('%s:%.4f ' % (tag, log_p))
            elif smooth == 2:
                # Good-Turing smoothing
                omitfile.write(tag)
                # if num < T:
                #     print N[tag]
                #     print dr[tag]
                #     print num,tag_freq[tag]
                #     omitfile.write(':%.4f ' % (math.log(dr[tag][num] / tag_freq[tag])))
                # else:
                omitfile.write(':%.4f ' %
                               (math.log(num * 1.0 / tag_freq[tag])))
        omitfile.write('\n')
    omitfile.close()
    infile.close()


def calcTransProb(TRAN_PROBFILE='ctb7_tran.txt', smooth=0, T=10):
    t_input = codecs.open(TRAN_PROBFILE, mode='r', encoding='utf8')
    t_out = codecs.open('ctb7_tranprob.txt', mode='w', encoding='utf8')
    print "Calculate the transition probability."
    t_out.write("#TRAN_PROB log_probability\n")
    is_first_line = True
    freq_sum = 0.
    tag_freq = {}
    N = {}
    ll = 0
    for line in t_input.readlines():
        ll += 1
        if is_first_line:
            is_first_line = False
            continue
        for i in range(T + 1):
            N[i] = 0.
        freq_sum = 0.
        tag_freq = {}
        raw = line.strip().split()
        tag1 = raw[0]
        for i in range(1, len(raw)):
            tag2, num = raw[i].split(':')
            num = int(num)
            freq_sum += num
            tag_freq[tag2] = num
            if num <= T:
                N[num] += 1
        # print "%d:" % ll,
        # print N
        if smooth == 2:
            curveTag = sum(1 if N[i] != 0 else 0 for i in range(1, T + 1))
            if curveTag > 1 and freq_sum > 30:
                theta = curveFit(N, T)
                dr = KatzGoodTuring(theta, N, T)
                # print dr
            else:
                # print the line that dont have enough data
                print "line %d does not have enough data to calculate." % ll
                dr = [1e-6 * freq_sum]
                for i in range(1, T):
                    dr.append(float(i))

        t_out.write(tag1 + ' ')
        for tag in TAGSET:
            freq = tag_freq[tag]
            t_out.write(tag + ':')
            if smooth == 0:
                # No smoothing tech used
                if freq == 0:
                    t_out.write('-inf ')
                else:
                    t_out.write('%.4f ' % (math.log(freq * 1.0 / freq_sum)))
            elif smooth == 1:
                # Laplace smoothing
                log_p = math.log((freq + 1.0) / (freq_sum + 37.0))
                t_out.write('%.4f ' % log_p)
            elif smooth == 2:
                # Good-Turing smoothing
                if freq < T:
                    t_out.write('%.4f ' % (math.log(dr[freq] / freq_sum)))
                else:
                    t_out.write('%.4f ' % (math.log(freq * 1.0 / freq_sum)))
        t_out.write('\n')
    print "Finished calculating transition probability."
    t_input.close()
    t_out.close()


def calcInitProb(INIT_PROBFILE='ctb7_init.txt', smooth=0, T=10):
    i_input = codecs.open(INIT_PROBFILE, mode='r', encoding='utf8')
    i_out = codecs.open('ctb7_initprob.txt', mode='w', encoding='utf8')
    print "Calculate the start probability."
    is_first_line = True
    freq_sum = 0.
    tag_freq = {}
    N = {}  # the good turing freq statistic
    for i in range(T + 1):
        N[i] = 0.
    for line in i_input.readlines():
        if is_first_line:
            is_first_line = False
            continue
        raw = line.strip().split()
        num = int(raw[1])
        tag_freq[raw[0]] = num
        freq_sum += num
        if num <= T:
            N[num] += 1

    # print N
    if smooth == 2:
        # Good-Turing smoothing, need to fit the gap between freq
        theta = curveFit(N, T)
        dr = KatzGoodTuring(theta, N, T)
        # print dr
    print "Writing start log_probability to the file."
    i_out.write("#INIT_PROB log_probability\n")

    for tag in TAGSET:
        freq = tag_freq[tag]
        i_out.write(tag + ' ')
        if smooth == 0:
            # No smoothing tech used
            if freq == 0:
                i_out.write('-inf\n')
            else:
                i_out.write('%.4f\n' % (math.log(freq * 1.0 / freq_sum)))
        elif smooth == 1:
            # Laplace smoothing
            log_p = math.log((freq + 1.0) / (freq_sum + 37.0))
            i_out.write('%.4f\n' % log_p)
        elif smooth == 2:
            # Good-Turing smoothing
            if freq < T:
                i_out.write('%.4f\n' % (math.log(dr[freq] / freq_sum)))
            else:
                i_out.write('%.4f\n' % (math.log(freq * 1.0 / freq_sum)))
    print "Finished calculating start probability."
    i_input.close()
    i_out.close()


def KatzGoodTuring(theta, N, T):
    K = T - 1
    for i in range(1, T + 1):
        # use fitted curve value to replace the origin value
        N[i] = theta[0] * math.pow(i, theta[1])
    # Print the freq after fit gap
    # print N
    dr = [0.0]
    for i in range(1, T):
        # r = (i + 1) * N[i + 1] / N[i]
        r = ((i + 1) * N[i + 1] / N[i] - i *
             ((1 + K) * N[K]) / N[1]) / (1 - (1 + K) * N[K] / N[1])
        dr[0] += (i - r)
        dr.append(r)
        # print "%d: r=%.4f g=%.4f" % (i, r, N[i])
    return dr


def curveFit(data, T):
    lnx = []
    lny = []
    for i in range(1, T + 1):
        if data[i] != 0:
            lnx.append(math.log(i))
            lny.append(math.log(data[i]))
    mean_x = sum(lnx) / len(lnx)
    mean_y = sum(lny) / len(lny)
    lxx = sum((x - mean_x)**2 for x in lnx)
    lxy = 0.0
    for i in range(len(lnx)):
        lxy += (lnx[i] - mean_x) * (lny[i] - mean_y)

    # print "lnx:", lnx
    # print "lny:", lny
    # print "lxx:", lxx
    # print "lxy:", lxy
    b1 = lxy / lxx
    b0 = mean_y - mean_x * b1
    # print "b0: ", b0
    # print "b1: ", b1
    return [math.exp(b0), b1]

if __name__ == '__main__':
    # getHmmModelInfo()
    # saveHMM()
    readTagFile()
    # calcInitProb(smooth=2, T=10)
    # calcTransProb(smooth=2, T=10)
    calcOmitProb(smooth=1, T=10)
