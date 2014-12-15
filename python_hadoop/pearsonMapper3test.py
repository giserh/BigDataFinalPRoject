#!/usr/bin/env python
'''
input : :Monday_21  1070_Forest Hills|37,Little Italy|1033
output: (forest hill,lillt itaky\t37,1033)
'''
import itertools, operator, sys
test = ['Monday_21\t22222_Hills|37,Little Italy|1033,uuuuuu|111111','Monday_21\t22222_bbbb|55,cccc|1033,dddd|111111']
def parseInput():
    for line in test:
    # for line in sys.stdin:
        values = line.strip('\n').split('\t')
        if len(values)>1: 
            yield values


def mapper():
    
    for values in parseInput():
        (sumcount,value_array) = values[1].split('_')
        valuelist = value_array.split(',')
        combination_result = itertools.combinations(valuelist,2)
        # trythis = map(lambda x :x[0].split('|')[0]+'|'+ x[1].split('|')[0],combination_result)
        # print trythis
        for combine in combination_result:
            item1_array = combine[0].split('|')
            item2_array = combine[1].split('|')
            print "%s\t%s" % (item1_array[0]+ '|' + item2_array[0], item1_array[1] + '|' + item2_array[1])
        # print '%s\t%s' % (key_array[0], output_value)

if __name__=='__main__':
    mapper()
