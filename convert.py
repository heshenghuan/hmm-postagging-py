#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 11:28:15 2016-03-29

@author: heshenghuan (heshenghuan@sina.com)
http://github.com/heshenghuan
"""

import codecs
import sys


def convert(filepath, outfile):
    src_file = codecs.open(filepath, mode='r', encoding='utf8')
    tgt_file = codecs.open(outfile, mode='w', encoding='utf8')
    num = 0
    print "Start convertion:"
    for line in src_file.readlines():
        raw_sent = line.strip().split()
        out_str = []
        for items in raw_sent:
            index = items.rfind('/')
            word = items[: index]
            out_str.append(word)
        for word in out_str:
            tgt_file.write(word)
            tgt_file.write(" ")
        tgt_file.write("\n")

        num += 1
        if num % 100 == 0:
            print ".",
            if num % 2000 == 0:
                print

    print "\nConvert done! Totally %d sentences" % num


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "ERROR: Not enough parameters!"
        print "Usage: python convert.py corpus_with_pos corpus_without_pos"
        sys.exit(0)
    convert(sys.argv[1], sys.argv[2])
