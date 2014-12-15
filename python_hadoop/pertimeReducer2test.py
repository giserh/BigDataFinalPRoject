#!/usr/bin/env python
import itertools, operator, sys

'''input : Monday_21 Forest Hills|37

output :Monday_21	Forest Hills|37, Little Italy|1033
'''
# test = ['Monday_21\tForest Hills|37\n','Monday_21\tLittle Italy|1033\n']

def parseInput():
	# for line in test:
	for line in sys.stdin:
		values = line.strip('\n').split('\t')
		if len(values)>1 and values[0]!='medallion': 
			yield values

def reducer():
	for key,values in itertools.groupby(parseInput(),operator.itemgetter(0)):
		output_combine = zip(*values)[1]
		sumcount =sum(map(lambda x: int(x.split('|')[1]),output_combine))
		# total_ride = map(methodcaller("split", "|"), output_combine)
		
		print '%s\t%s' % (key,str(sumcount)+'_'+','.join(output_combine))

if __name__=='__main__':
	reducer()          