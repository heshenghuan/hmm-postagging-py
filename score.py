#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 15:07:03 2016-05-23

@author: heshenghuan (heshenghuan@sina.com)
http://github.com/heshenghuan
"""

import codecs
import sys


def score(GOLDFILE, GIVEFILE, OUTFILE):
    correct_num = 0
    given_num = 0
    gold_num = 0
    goldfile = codecs.open(GOLDFILE, mode='r', encoding='utf8')
    givefile = codecs.open(GIVEFILE, mode='r', encoding='utf8')
    score_file = codecs.open(OUTFILE, mode='w', encoding='utf8')

    goldlines = goldfile.readlines()
    givelines = givefile.readlines()

    if len(goldlines) != len(givelines):
        print "ERROR: The length of givefile not equal to goldfile."
        print "       Check if the file is given wrong."
    else:
        for i in range(len(goldlines)):
            gold = goldlines[i].strip().split()
            give = givelines[i].strip().split()
            given_num += len(gold)
            gold_num += len(give)
            if len(gold) == 0 and len(give) == 0:
                continue
            m = min(len(gold), len(give))
            right = 0
            for j in range(m):
                index = gold[j].rfind('/')
                gold_word = gold[j][:index]
                gold_tag = gold[j][index + 1:]
                index = give[j].rfind('/')
                give_word = give[j][:index]
                give_tag = give[j][index + 1:]
                score_file.write(gold[j] + "    " + give[j] + '\n')

                if gold_word == give_word and gold_tag == give_tag:
                    correct_num += 1
                    right += 1
            if len(gold) > len(give):
                for j in range(m + 1, len(gold)):
                    score_file.write(gold[j] + "    >\n")
            elif len(gold) < len(give):
                for j in range(m + 1, len(give)):
                    score_file.write(">    %s\n" % give[j])
            p = right * 1.0 / len(give)
            r = right * 1.0 / len(gold)
            f = 2 * (p * r) / (p + r) if (p + r) != 0 else 0.0
            score_file.write(
                "Precision: %.4f  Recall: %.4f  F1-Measure: %.4f\n" % (p, r, f))

        p = correct_num * 1.0 / given_num
        r = correct_num * 1.0 / gold_num
        f = 2 * (p * r) / (p + r)
        print "Precision: %.4f" % p
        print "Recall: %.4f" % r
        print "F1-Measure %.4f" % f
        score_file.write("\n\nSummary:\n")
        score_file.write(
            "Precision: %.4f  Recall: %.4f  F1-Measure: %.4f\n" % (p, r, f))

    goldfile.close()
    givefile.close()


if __name__ == '__main__':
    # print sys.argv
    score(sys.argv[1], sys.argv[2], sys.argv[3])
