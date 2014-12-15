#!/usr/bin/env python
import itertools, operator, sys
def parseInput():
    for line in sys.stdin:
        values = line.strip('\n').split('\t')
        if len(values)>1: 
            yield values

def mapper():
    for values in parseInput():
        (sumcount,value_array) = values[1].split('_')
        valuelist = value_array.split(',')
        combination_result = itertools.combinations(valuelist,2)

        for combine in combination_result:
            item1_array = combine[0].split('|')
            item2_array = combine[1].split('|')
            print "%s\t%s" % (item1_array[0]+ '|' + item2_array[0], item1_array[1] + '|' + item2_array[1])

if __name__=='__main__':
    mapper()
