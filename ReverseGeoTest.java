package org.geotools.tutorial.quickstart;

import com.sun.xml.internal.bind.v2.runtime.Name;
import com.vividsolutions.jts.geom.Coordinate;
import com.vividsolutions.jts.geom.GeometryFactory;
import com.vividsolutions.jts.geom.Point;
import org.geotools.data.FileDataStore;
import org.geotools.data.FileDataStoreFinder;
import org.geotools.data.shapefile.ShapefileDataStore;
import org.geotools.data.shapefile.ShapefileDataStoreFactory;
import org.geotools.data.simple.SimpleFeatureCollection;
import org.geotools.data.simple.SimpleFeatureIterator;
import org.geotools.data.simple.SimpleFeatureSource;
import org.geotools.filter.text.cql2.CQL;
import org.geotools.geometry.jts.JTSFactoryFinder;
import org.geotools.swing.data.JFileDataStoreChooser;
import org.opengis.feature.simple.SimpleFeature;
import org.opengis.filter.Filter;

import java.beans.Expression;
import java.util.*;
import javax.activation.FileDataSource;
import java.io.File;

/**
 * Created by xisu on 11/26/14.
 */
public class ReverseGeoTest {

    public static void main(String[] args)throws Exception {

        double longitude = -73.97;
        double latitude = 40.78;
        GetNeighborhoodName getNeighborhoodName = new GetNeighborhoodName();
        String name = getNeighborhoodName.GetName(longitude, latitude);
        System.out.println(name);
    }
    public static class GetNeighborhoodName {
        public static String GetName(Double longitude, Double latitude)throws Exception{

            String path = "ZillowNeighborhoods-NY.shp";
            File file = new File(path);
            if(file == null){
                return null;
            }
            GeometryFactory  geometryFactory = JTSFactoryFinder.getGeometryFactory(null);
            Point point = geometryFactory.createPoint(new Coordinate(longitude,latitude));
            FileDataStore dataStore = FileDataStoreFinder.getDataStore(file);
            SimpleFeatureSource featureSource = dataStore.getFeatureSource();
//        String featureString = featureSource.getFeatures().toString();

            Filter filter = CQL.toFilter("CONTAINS(the_geom, "+ point +")");
            SimpleFeatureCollection collection = featureSource.getFeatures(filter);
            SimpleFeatureIterator featureIterator = collection.features();
            String featureName="";
            try{
                while(featureIterator.hasNext()){
                    SimpleFeature feature = featureIterator.next();
                    String name = "NAME";
                    featureName = feature.getAttribute(name).toString();
                }
            }finally{
                featureIterator.close();
                return featureName;

            }
        }

    }


//        System.out.println(featureString);
//        GeometryFactory geometryFactory = new GeometryFactory();


}
