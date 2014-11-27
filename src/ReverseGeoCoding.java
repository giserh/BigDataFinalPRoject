

import com.vividsolutions.jts.geom.Coordinate;
import com.vividsolutions.jts.geom.GeometryFactory;
import com.vividsolutions.jts.geom.Point;

import org.geotools.data.FileDataStore;
import org.geotools.data.FileDataStoreFinder;
import org.geotools.data.simple.SimpleFeatureCollection;
import org.geotools.data.simple.SimpleFeatureIterator;
import org.geotools.data.simple.SimpleFeatureSource;
import org.geotools.filter.text.cql2.CQL;
import org.geotools.geometry.jts.JTSFactoryFinder;
import org.opengis.feature.simple.SimpleFeature;
import org.opengis.filter.Filter;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.mapreduce.Mapper.Context;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

import java.io.IOException;
import java.io.File;

/**
 * Created by xisu on 11/26/14.
 */
public class ReverseGeoCoding{
	
	
	public static class Map extends Mapper<LongWritable, Text, Text, IntWritable> {

		private static final int PICKUP_LONGITUDE = 10;
		private static final int PICKUP_LATITUDE = 11;
		private static final IntWritable one = new IntWritable(1);
		//        private Text word = new Text();

		public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
			String line = value.toString();
			if (!line.split(",")[0].equals("medallion")) {
				Double pickupLongitude = Double.parseDouble(line.split(",")[PICKUP_LONGITUDE]);
				Double pickupLatitude = Double.parseDouble(line.split(",")[PICKUP_LATITUDE]);
//				GetNeighborhoodName getNeighborhoodName = new GetNeighborhoodName();
				String name = "";
				try{
					name = GetName(pickupLongitude, pickupLatitude);

				}catch(Exception e){
					System.out.println(e.getMessage());
				}
				//                word.set(name);
//				System.out.println(name);
				context.write(new Text(name), one);
			}
		}
		@SuppressWarnings("finally")
		public String GetName(Double longitude, Double latitude) throws Exception {

            String path = "/Users/xisu/Documents/NYU-CS/NYU-POLY/bigdata/final_project/ZillowNeighborhoods-NY/ZillowNeighborhoods-NY.shp";
            File file = new File(path);
            GeometryFactory geometryFactory = JTSFactoryFinder.getGeometryFactory(null);
            Point point = geometryFactory.createPoint(new Coordinate(longitude, latitude));
            FileDataStore dataStore = FileDataStoreFinder.getDataStore(file);
            SimpleFeatureSource featureSource = dataStore.getFeatureSource();
//        String featureString = featureSource.getFeatures().toString();

            Filter filter = CQL.toFilter("CONTAINS(the_geom, " + point + ")");
            SimpleFeatureCollection collection = featureSource.getFeatures(filter);
            SimpleFeatureIterator featureIterator = collection.features();
            String featureName = "";
            String name = "NAME";
            try {
                while (featureIterator.hasNext()) {
                    SimpleFeature feature = featureIterator.next();
                   
                    featureName = feature.getAttribute(name).toString();
                }
            } finally {
                featureIterator.close();
                return featureName; 
                

            }
        }

	}
	 public static class Reduce extends Reducer<Text, IntWritable, Text, IntWritable> {

		 public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
			 int sum = 0;
			 for (IntWritable val:values) {
				 sum += val.get();
			 }
			 context.write(key, new IntWritable(sum));
		 }
	 }
	
	
	 public static void main(String[] args)throws Exception {
		 
		 
		 Configuration conf = new Configuration();
		 Job job = new Job(conf, "neighorhood");
		 job.setJarByClass(ReverseGeoCoding.class);

		 job.setOutputKeyClass(Text.class);
		 job.setOutputValueClass(IntWritable.class);

		 job.setMapperClass(Map.class);
		 job.setReducerClass(Reduce.class);

		 job.setInputFormatClass(TextInputFormat.class);
		 job.setOutputFormatClass(TextOutputFormat.class);
		 job.setNumReduceTasks(1);
		 FileInputFormat.addInputPath(job, new Path(args[0]));
		 FileOutputFormat.setOutputPath(job, new Path(args[1]));

		 job.waitForCompletion(true);
	}

	
	
}
   
//		public int run(String[] args) throws Exception
//		{
//			if(args.length !=2) {
//				System.err.println("Usage: MaxTemperatureDriver <input path> <outputpath>");
//				System.exit(-1);
//			}
//			Job job = new Job();
//			job.setJarByClass( ReverseGeoCoding.class);
//			job.setJobName("NY neighborhood");
//			
//			FileInputFormat.addInputPath(job, new Path(args[0]));
//			FileOutputFormat.setOutputPath(job,new Path(args[1]));
//			
//			job.setMapperClass(Map.class);
//			job.setReducerClass(Reduce.class);
//			
//			job.setOutputKeyClass(Text.class);
//			job.setOutputValueClass(IntWritable.class);
//			System.exit(job.waitForCompletion(true) ? 0:1);
//			boolean success = job.waitForCompletion(true);
//			return success ? 0 : 1;
//		}
//		 public static void main(String[] args) throws Exception {
//			 ReverseGeoCoding driver = new  ReverseGeoCoding();
//		    	int exitCode = ToolRunner.run(driver, args);
//		    	System.exit(exitCode);
//		 }
//}

  
   

//   
//        
    

