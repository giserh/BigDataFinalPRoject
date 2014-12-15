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
def getWeekday(strdate):
    dt_format = datetime.strptime(strdate,"%Y-%m-%d %H:%M:%S")
    weekday = dt_format.strftime("%A")
    hour = dt_format.strftime("%H")
    return weekday+'_'+hour

def mapper():
    PICKUP_TIME = 5
    index = rtree.Index()
    neighborhoods = []
    readNeighborhood('ZillowNeighborhoods-NY.shp', index, neighborhoods)
    agg = {}
    for values in parseInput():
        if values[10] and values[11] and values[12] and values[13]:
            pickup_location = (float(values[10]), float(values[11]))
            pickup_neighborhood = findNeighborhood(pickup_location, index, neighborhoods)
            if pickup_neighborhood!=-1:

                pickup_neigh_name = neighborhoods[pickup_neighborhood][0]
                
                
                if(pickup_neigh_name == 'Upper East Side' or pickup_neigh_name == 'Upper West Side' or pickup_neigh_name == 'Chelsea' ):
                    pickup_time =int(values[PICKUP_TIME][11:13])
                    drop_location = (float(values[12]), float(values[13]))
                    drop_neighborhood = findNeighborhood(drop_location,index,neighborhoods)
                    drop_neigh_name = neighborhoods[drop_neighborhood][0]
                    key = pickup_neigh_name +"|"+ drop_neigh_name
                    

                    if(pickup_time > 17 and pickup_time < 20 ):

                        agg[key] = agg.get(key , 0) + 1
                    else:
                        agg[key] = agg.get(key , 0) + 0
                        

                if(pickup_neigh_name == 'East Village' or pickup_neigh_name == 'Lower East Side' or pickup_neigh_name == 'West Village' ):
                    pickup_time =int(values[PICKUP_TIME][11:13])
                    drop_location = (float(values[12]), float(values[13]))
                    drop_neighborhood = findNeighborhood(drop_location,index,neighborhoods)
                    drop_neigh_name = neighborhoods[drop_neighborhood][0]
                    key = pickup_neigh_name +"|"+ drop_neigh_name
                    agg[key] = agg.get(key , 0)

                    if(pickup_time > 21 or pickup_time < 2  ):
                        agg[key] = agg.get(key , 0) + 1
                    else:
                        agg[key] = agg.get(key , 0) + 0

    for item in agg.iteritems():
        print '%s\t%s' % (item[0], item[1])

if __name__=='__main__':
    mapper()
