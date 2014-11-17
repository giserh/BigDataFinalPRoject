import java.io.IOException;
import java.util.*;
import java.text.*;
import java.util.Calendar;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

public class WeekTimeActivity {

	public static class Map extends Mapper<LongWritable, Text, Text, IntWritable> {

		private static final int pickUpTime = 5;
		private static final IntWritable one = new IntWritable(1);

		private static String getWeek(String sdate) {
			SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd");
			ParsePosition pos = new ParsePosition(0);
			Date day = formatter.parse(sdate, pos);
			Calendar c = Calendar.getInstance();
			c.setTime(day);
			return new SimpleDateFormat("EEEE").format(c.getTime());
		}

		public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
			String line = value.toString();
			if (!line.split(",")[0].equals("medallion")) {
				String dayOfWeek = getWeek(line.split(",")[pickUpTime]);
				String tm = line.split(",")[pickUpTime].substring(11, 13);
				context.write(new Text(dayOfWeek + " " + tm), one);
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

	public static void main(String[] args) throws Exception {

		Configuration conf = new Configuration();
		Job job = new Job(conf, "weektimeactivity");
		job.setJarByClass(WeekTimeActivity.class);

		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(IntWritable.class);

		job.setMapperClass(Map.class);
		job.setReducerClass(Reduce.class);

		job.setInputFormatClass(TextInputFormat.class);
		job.setOutputFormatClass(TextOutputFormat.class);

		FileInputFormat.addInputPath(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));

		job.waitForCompletion(true);
	}
}