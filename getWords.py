#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 13:44:32 2016-06-07

@author: heshenghuan (heshenghuan@sina.com)
http://github.com/heshenghuan
"""

import codecs
import sys


def getWords(corpus, output):
    read = codecs.open(corpus, mode="r", encoding='utf8')
    write = codecs.open(output, mode="w", encoding="utf8")

    words_dict = set()
    num = 0
    print "Reading corpus and doing statistical work."
    for line in read.readlines():
        raw = line.strip()
        num += 1
        if num % 500 == 0:
            print '.',
            if num % 5000 == 0:
                print '\t%d sentences.' % num
        if raw == "":
            continue
        else:
            words = raw.split()
            for w in words:
                words_dict.add(w)

    print "\nStatistics finished. Totally %d lines." % num
    print "\nWritting words to output_file."
    num = 0
    for w in words_dict:
        num += 1
        if num % 500 == 0:
            print '.',
            if num % 5000 == 0:
                print '\t%d words.' % num
        write.write(w + '\n')
    print "\nTotally %d words have been written to output_file." % num


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "ERROR: Not enough parameters!"
        print "Usage: python getWords.py corpus_file output_file"
        sys.exit(0)
    getWords(sys.argv[1], sys.argv[2])
