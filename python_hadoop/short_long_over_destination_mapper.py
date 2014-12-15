#!/usr/bin/env python
import sys
sys.path.append('.')
import matplotlib
matplotlib.use('Agg')
from matplotlib.path import Path
from rtree import index as rtree
import numpy, shapefile, time
from datetime import datetime, date,time

def findNeighborhood(location, index, neighborhoods):
    match = index.intersection((location[0], location[1], location[0], location[1]))
    for a in match:
        if any(map(lambda x: x.contains_point(location), neighborhoods[a][1])):
            return a
    return -1

def readNeighborhood(shapeFilename, index, neighborhoods):
    sf = shapefile.Reader(shapeFilename)
    for sr in sf.shapeRecords():
        if sr.record[1] not in ['New York', 'Kings', 'Queens', 'Bronx']: continue
        paths = map(Path, numpy.split(sr.shape.points, sr.shape.parts[1:]))
        bbox = paths[0].get_extents()
        map(bbox.update_from_path, paths[1:])
        index.insert(len(neighborhoods), list(bbox.get_points()[0])+list(bbox.get_points()[1]))
        neighborhoods.append((sr.record[3], paths))
    neighborhoods.append(('UNKNOWN', None))

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

def mapper():
    index = rtree.Index()
    neighborhoods = []
    readNeighborhood('ZillowNeighborhoods-NY.shp', index, neighborhoods)
    agg = {}
    PICKUP_TIME = 5
    DROP_TIME = 6
    for values in parseInput():
        if values[12] and values[13] and values[PICKUP_TIME] and values[DROP_TIME]:

            minutes_diff = getMinutesDiff(values[PICKUP_TIME],values[DROP_TIME])

            drop_location = (float(values[12]), float(values[13]))
            drop_neighborhood = findNeighborhood(drop_location,index,neighborhoods)

            if drop_neighborhood !=-1:
                drop_neigh_name = neighborhoods[drop_neighborhood][0]
                if minutes_diff <= 15:
                    key = "M15|"+drop_neigh_name
                if minutes_diff >15 and minutes_diff <=30:
                    key = "M30|"+drop_neigh_name
                if minutes_diff > 30 and minutes_diff <=60:
                    key = "M60|"+drop_neigh_name
                if minutes_diff >60:
                    key= "H1|"+drop_neigh_name
                agg[key] = agg.get(key, 0) + 1

    for item in agg.iteritems():
        print '%s\t%s' % (item[0], item[1])

if __name__=='__main__':
    mapper()
