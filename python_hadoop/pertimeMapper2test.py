#!/usr/bin/env python
import sys
import matplotlib
import itertools, operator
'''
input :Monday_21|Forest Hills   37
        Monday_21|Greenwich Village 5249

output : Monday_21 "Forest Hills|37"
'''
def parseInput():
    for line in sys.stdin:
        values = line.strip('\n').split('\t')
        if len(values)>1 and values[0]!='medallion': 
            yield values


def mapper():
    
    for values in parseInput():
        key_array = values[0].split('|')
        output_value = key_array[1] + '|'+values[1]
        print '%s\t%s' % (key_array[0], output_value)

if __name__=='__main__':
    mapper()
