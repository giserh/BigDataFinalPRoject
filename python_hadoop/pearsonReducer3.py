#!/usr/bin/env python
import itertools, operator, sys, math
from math import sqrt, log, exp

CONFIDENCE = 1.96
def parseInput():
    for line in sys.stdin:
        values = line.strip('\n').split('\t')
        yield values


def fisher_z_transform(r):
    if 1+r != 0 and r != 1:
        z = 0.5 * (log((1+r)/(1-r)))
        return z
def standard_error(n):
    if n > 3:
        strr = 1/(sqrt(n-3))
        return strr
    else:
        return 0
def inverse_to_r(z):
    r = (exp(2*z) - 1)/(exp(2*z) + 1)
    return r
def pearsonSimilarity(x,y,xx,yy,xy,n):
    num = float(xy-x*y/n)
    denom = float(sqrt(xx - math.pow(x,2)/n) * sqrt(yy - math.pow(y,2)/n))
    pearson_simi = 0
    if denom != 0:
        pearson_simi = round(num / denom, 5)
    return pearson_simi

def reducer():
    agg = {}
    for key, value in itertools.groupby(parseInput(), operator.itemgetter(0)):
        (item1,item2) = key.split('|')
        value_region = zip(*value)[1]
        (sumX, sumY, sumXX, sumYY, sumXY, count) = (0, 0, 0, 0, 0, 0)
        for pare in value_region:
            (x,y) = map(int,pare.split('|'))
            sumX += x
            sumY += y
            sumXX += x * x
            sumYY += y * y
            sumXY += x * y
            count += 1
        similarity = pearsonSimilarity(sumX, sumY, sumXX, sumYY, sumXY, count)
        print "%s\t%s\t%s\t%s" % (item1, item2, similarity, count)

if __name__=='__main__':
    reducer()