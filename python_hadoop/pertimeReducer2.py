#!/usr/bin/env python
import itertools, operator, sys

def parseInput():
    for line in sys.stdin:
        values = line.strip('\n').split('\t')
        yield values

def reducer():
    agg = {}
    for key,values in itertools.groupby(parseInput(),operator.itemgetter(0)):
        output_combine = zip(*values)[1]
        sumcount =sum(map(lambda x: int(x.split('|')[1]),output_combine))
        
        print '%s\t%s' % (key,str(sumcount)+'_'+','.join(output_combine))

if __name__=='__main__':
    reducer()