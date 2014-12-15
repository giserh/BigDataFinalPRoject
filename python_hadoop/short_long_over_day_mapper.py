#!/usr/bin/env python
import sys
import itertools, operator
from datetime import datetime

def parseInput():
    for line in sys.stdin:
        line = line.strip('\n')
        values = line.split(',')
        if len(values)>1 and values[0]!='medallion': 
            yield values
def getMinutesDiff(pick_time,drop_time):
    pick = datetime.strptime(pick_time,"%Y-%m-%d %H:%M:%S")
    drop = datetime.strptime(drop_time,"%Y-%m-%d %H:%M:%S") 
  
    return int((drop - pick).total_seconds()/60)
# def getDay(pick_time):
#     pick = datetime.strptime(pick_time,"%Y-%m-%d %H:%M:%S")
#     return 
def mapper():
    agg = {}
    PICKUP_TIME = 5
    DROP_TIME = 6
    for values in parseInput():
        pick = values[PICKUP_TIME]
        drop = values[DROP_TIME]
        minutes_diff = getMinutesDiff(pick,drop)
        day = pick[5:10]
        if minutes_diff <= 15:
            key = "M15|"+day
        if minutes_diff >15 and minutes_diff <=30:
            key = "M30|"+day
        if minutes_diff > 30 and minutes_diff <=60:
            key = "M60|"+day
        if minutes_diff >60:
            key= "H1|"+day
        agg[key] = agg.get(key, 0) + 1
            
    for item in agg.iteritems():
        print '%s\t%s' % (item[0], item[1])
        

if __name__=='__main__':
    mapper()