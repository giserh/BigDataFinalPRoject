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
        drop_location = (float(values[12]), float(values[13]))
        Month = values[5][5:7]

        drop_neighborhood = findNeighborhood(drop_location, index, neighborhoods)
        time_neighbor_key = Month+'|'+str(drop_neighborhood)
        if drop_neighborhood!=-1:
            agg[time_neighbor_key] = agg.get(time_neighbor_key , 0) + 1

    for item in agg.iteritems():
        key_array = item[0].split('|')
        neighborhood_name = neighborhoods[int(key_array[1])][0]
        output_key = key_array[0]+'|'+ neighborhood_name
        print '%s\t%s' % (output_key, item[1])

if __name__=='__main__':
    mapper()
