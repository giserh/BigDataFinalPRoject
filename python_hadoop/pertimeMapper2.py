#!/usr/bin/env python
import sys
import itertools, operator

def parseInput():
    for line in sys.stdin:
        values = line.strip('\n').split('\t')
        if len(values)>1: 
            yield values


def mapper():
    agg = {}
    for values in parseInput():
        key_array = values[0].split('|')
        output_value = key_array[1] + '|'+values[1]
        print '%s\t%s' % (key_array[0], output_value)

if __name__=='__main__':
    mapper()
