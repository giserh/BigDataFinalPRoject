#!/usr/bin/env python
import itertools, operator, sys, math
from math import sqrt, log, exp
'''
input
['Hills|Little Italy\t37|1033\n',Hills|Little Italy\t40|1000\n','Hills|Little Italy\t3|103','Hills|uuuuuu\t37|111111\n']
Hills|Little Italy  33|103
Hills|uuuuuu    37|111111
Little Italy|uuuuuu 1033|111111

'''
test = ['Hills|Little Italy\t37|1033\n','Hills|Little Italy\t40|1000\n','Hills|Little Italy\t3|103','Hills|uuuuuu\t37|111111\n']
CONFIDENCE = 1.96
# respomnse 0.95
def parseInput():
    for line in test:
    # for line in sys.stdin:
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
    if pearson_simi > 0.99999:
        pearson_simi = 0.99999
    if pearson_simi < -0.99999:
        pearson_simi = -0.99999
    fisher_lower_boundry = inverse_to_r(fisher_z_transform(pearson_simi) - standard_error(n) * CONFIDENCE)
    fisher_upper_boundry = inverse_to_r(fisher_z_transform(pearson_simi) + standard_error(n) * CONFIDENCE)

    if fisher_lower_boundry * pearson_simi <= 0:
        fisher_lower_boundry = 0
    if fisher_lower_boundry * fisher_upper_boundry < 0:
        fisher_lower_boundry = min(abs(fisher_lower_boundry),abs(fisher_upper_boundry))
    else:
        fisher_lower_boundry = min(fisher_lower_boundry,fisher_upper_boundry)
    return fisher_lower_boundry



def reducer():
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
        print "%s_%s %s %s" % (item1, item2, similarity, count)

if __name__=='__main__':
    reducer()