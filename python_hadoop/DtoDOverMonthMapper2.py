#!/usr/bin/env python
import sys
sys.path.append('.')
import matplotlib
matplotlib.use('Agg')
from matplotlib.path import Path
from rtree import index as rtree
import numpy, shapefile, time

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

def mapper():
    index = rtree.Index()
    neighborhoods = []
    readNeighborhood('ZillowNeighborhoods-NY.shp', index, neighborhoods)
    agg = {}
    for values in parseInput():
        if values[10] and values[11] and values[12] and values[13]:
            pickup_location = (float(values[10]), float(values[11]))
            drop_location = (float(values[12]), float(values[13]))
            pickup_neighborhood = findNeighborhood(pickup_location, index, neighborhoods)
            drop_neighborhood = findNeighborhood(drop_location,index,neighborhoods)

            Month = values[5][5:7]
            pickup_neigh_name = neighborhoods[pickup_neighborhood][0]
            drop_neigh_name = neighborhoods[drop_neighborhood][0]
            if pickup_neighborhood!=-1 and drop_neighborhood !=-1:
                d_to_d = Month + '|' + pickup_neigh_name + '|' + drop_neigh_name 
                agg[d_to_d] = agg.get(d_to_d, 0) + 1

    for item in agg.iteritems():
        print '%s\t%s' % (item[0], item[1])

if __name__=='__main__':
    mapper()
